import json
from channels import Group
from channels.auth import channel_session
from django.forms.models import model_to_dict
from django.core import serializers


@channel_session
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})

    Group('comments').add(message.reply_channel)


def ws_send_comment_changed(comment, created):
    obj = serializers.serialize('json', [ comment, ])
    Group('comments').send({
        'text': json.dumps({
            # 'comment': model_to_dict(comment),
            'comment': obj,
            'created': created,
        })
    })
    print("I've sent " + str(comment) + " and " + str(created))


@channel_session
def ws_disconnect(message):
    Group('comments').discard(message.reply_channel)
