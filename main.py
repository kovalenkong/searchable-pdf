import argparse
import logging
import multiprocessing
from io import BytesIO
from multiprocessing import Process

import pytesseract
from pdf2image import convert_from_path
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfReader

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s (PID %(process)d): %(message)s'
))
logger.addHandler(handler)


def pdf_to_ocr(
        pages: dict,
        input_filename: str,
        page_from: int,
        page_to: int,
        lang: str
):
    logger.info(
        'starting to convert the pdf '
        f'(pages {page_from} to {page_to})'
    )
    images = convert_from_path(
        input_filename,
        first_page=page_from,
        last_page=page_to
    )
    for idx, image in enumerate(images, page_from):
        im = BytesIO()
        im.name = '_.jpg'
        image.save(im)
        page = pytesseract.image_to_pdf_or_hocr(image, lang=lang)
        pages[idx] = PdfFileReader(BytesIO(page))
        logger.debug(f'page {idx} converted')


def get_number_of_pages_in_pack(total_pages: int, processes: int) -> int:
    # 10 pages per process
    return min((
        max((total_pages // processes, 10)),
        total_pages
    ))


def configure_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='PDF to searchable pdf')
    parser.add_argument(
        'input',
        help='input filename (pdf type)'
    )
    parser.add_argument(
        'output',
        help='output filename (with pdf extension)'
    )
    parser.add_argument(
        '-l',
        '--languages',
        type=str,
        default='eng',
        help='list of languages, separated by +'
    )
    parser.add_argument(
        '-p',
        '--processes',
        type=int,
        default=10,
        help='max processes'
    )
    return parser


def main():
    parser = configure_parser()
    args = parser.parse_args()

    doc = PdfReader(args.input)
    page_from = 1
    page_to = doc.numPages
    pages_in_package = get_number_of_pages_in_pack(page_to, args.processes)

    manager = multiprocessing.Manager()
    pages = manager.dict()

    processes = [
        Process(
            target=pdf_to_ocr,
            kwargs={
                'pages': pages,
                'input_filename': args.input,
                'page_from': i,
                'page_to': end if (
                                      end := i + pages_in_package
                                  ) <= page_to else page_to + 1,
                'lang': args.languages,
            }
        ) for i in range(page_from, page_to + 1, pages_in_package)
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    logger.info('merging pages')

    merger = PdfFileMerger()
    for _, page in sorted(pages.items(), key=lambda i: i[0]):
        merger.append(page)

    merger.write(args.output)


if __name__ == '__main__':
    main()
