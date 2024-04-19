
from .common.factory import DefaultToolFactoryRegistry
from .tools import pdf

toolfactory = DefaultToolFactoryRegistry()
toolfactory.register('pdf', pdf.factory)
toolfactory.register('csv', pdf.factory)
toolfactory.register('image', pdf.factory)
toolfactory.register('video', pdf.factory)
toolfactory.register('AI', pdf.factory)

