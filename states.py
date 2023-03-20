from aiogram.dispatcher.filters.state import StatesGroup, State


class crypto_st(StatesGroup):
    crypto = State()


class add_acc_st(StatesGroup):
    add_new_acc_step1 = State()
    add_new_acc_step2 = State()
    add_new_acc_step3 = State()
    add_new_acc_step4 = State()
    add_new_acc_step5 = State()
    

class get_acc_st(StatesGroup):
    my_acc_step1 = State()
    my_acc_step2 = State()
    worker_acc_step1 = State()
    worker_acc_step2 = State()


class delete_acc_st(StatesGroup):
    delete_acc_step1 = State()