from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from random import randint
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings


def play_random_numbers(user_num):
    bot_num = randint(user_num - 10, user_num + 10)
    if user_num > bot_num:
        message = f'Кожаный, ты выбрал число {user_num}, а моё число:'
        f'{bot_num}! Твоя взяла!'
    elif user_num == bot_num:
        message = f'Число юзера: {user_num}, число бота: {bot_num}. Ничья!'
    else:
        message = f'Свершилось, кожаный! Ты выбрал число {user_num}, '
        f'а я выбрал {bot_num}! Я победил! Уга-га-га!'
    return message


def main_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Отправь пёсика', 'Отправь peace'],
            [KeyboardButton('Моя геолокация', request_location=True)],
            ['Заполнить анкету-отзыв о боте']
            ]
            )


def has_object_on_img(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])

    response = app.PostModelOutputs(request, metadata=metadata)
    return check_responce_for_object(response, object_name)


def check_responce_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.85:
                return True
    else:
        print(f"Ошибка распознавания: {response.outputs[0].status.details}")

    return False


if __name__ == '__main__':
    print(has_object_on_img('/home/alexhope/pythonProject/LP lessons/'
                            'L1/newbot/images/dog3.jpg', 'dog'))
    print(has_object_on_img('/home/alexhope/pythonProject/LP lessons/'
                            'L1/newbot/images/peace1.jpeg', 'dog'))
