# from .waterstones_base_service import InnerService
#
#
# class NewBooksService(InnerService):
#     def __init__(self, url):
#         self._url = url
#
#     def get_data(self):
#         lst2 = super().get_data()
#
#         bom = lst2[1:7]
#         bom.pop(2)  # removing 'special' section
#
#         return [self.get_book_details(pair) for pair in bom]
