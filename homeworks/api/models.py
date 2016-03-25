import datetime
from validate_email import validate_email


class Api:
    def __init__(self, data):
        self.data = data
        self.res = []

    def val_order_count(self, minimum=1, maximum=5):
        return minimum <= int(self.data['order']['count']) <= maximum

    def val_order_in_list(self):
        return self.data['order']['product_name'] in self.ORDER_LIST

    def val_is_name(self):
        return 'name' in self.data['client'].keys()

    def val_address(self):
        return len(self.data['address']) > 0

    def check(self):
        for validator in [method for method in self.__dir__() if method.startswith('val_')]:
            func = getattr(self, validator)
            self.res.append((func(), validator))
        return self.res

    def save(self):
        with open('order.txt', 'a') as outfile:
            outfile.write(str(self.data) + '\n')


class ApiV1(Api):
    def __init__(self, data):
        Api.__init__(self, data)
        self.ORDER_LIST = ['book', 'game']


class ApiV2(Api):
    def __init__(self, data):
        Api.__init__(self, data)
        self.ORDER_LIST = ['book', 'game', 'movie', 'music']

    def val_order_count(self, minimum=1, maximum=10):
        return Api.val_order_count(self, minimum, maximum)

    def val_is_name(self):
        return len(self.data['client']['name']) > 0

    def val_email(self):
        return validate_email(self.data['client']['email'])

    def val_address(self):
        return len(self.data['client']['address']) > 0

    def save(self):
        Api.save(self)
        with open("order.log", 'a') as f:
            f.write(str(datetime.datetime.now()) + " New order \n")
