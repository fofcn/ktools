
from .pdftoolfactory import PdfToolFactory
from .pdfsplitter import PdfSplitter

factory = PdfToolFactory()
factory.register_tool('splitter', PdfSplitter())

