import json
from django.db.models import fields
import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from users.models import UserProfile
from graphql_relay.node.node import from_global_id


from . import models


class UserType(DjangoObjectType):
    full_name = graphene.String(source='full_name')

    class Meta:
        model = get_user_model()
        fields = ('username', 'is_staff', 'email',
                  'full_name', 'title', 'profile', )
        interfaces = (graphene.Node, )


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
        # fields = ('id', 'profile_picture', 'recent_time', )
        interfaces = (graphene.Node, )


class MessageType(DjangoObjectType):
    class Meta:
        model = models.Message
        # fields = ('id', 'message', 'creation_date', 'user')
        interfaces = (graphene.Node, )
        convert_choices_to_enum = True
        
    extra_field = graphene.String()

    def resolve_extra_field(root, info):
        return 'I am extra field !'

class MessageConnection(graphene.relay.Connection):
    class Meta:
        node = MessageType
        

class Query(graphene.ObjectType):
    all_messages = graphene.List(MessageType, priority=graphene.String())
    # all_messages = graphene.relay.ConnectionField(MessageConnection, priority=graphene.String())
    message = graphene.Field(MessageType, id=graphene.ID())
    current_user = graphene.Field(UserType)

    def resolve_all_messages(self, info, **kwargs):
        # print(f'info: {info}')
        # print(f'context: {info.context}')
        # print(f'user: {info.context.user}')
        priority = kwargs.get('priority')
        # if info and info.context.user.is_authenticated:
        #     if not priority:
        #         return models.Message.objects.all()
        #     else:
        #         return models.Message.objects.filter(priority=priority)
        # else:
        #     return models.Message.objects.none()
        if not priority:
            return models.Message.objects.all()
        else:
            return models.Message.objects.filter(priority=priority)
    
    def resolve_message(self, info, id):
        rid = from_global_id(id)
        return models.Message.objects.get(pk=rid[1])
    
    def resolve_current_user(self, info, **kwargs):
        if not info:
            req = kwargs.get('req')
            user = req.user
        else:
            user = info.context.user
        if not user.is_authenticated:
            return None
        return user


class CreateMessageMutation(graphene.Mutation):
    class Arguments:
        message = graphene.String(required=True)
        priority = graphene.String()

    status = graphene.Int()
    formErrors = graphene.String()
    message = graphene.Field(MessageType)

    def mutate(root, info, message, priority=None):
        if not info.context.user.is_authenticated:
            return CreateMessageMutation(status=403)
        # message = message.strip() if message and len(message.strip()) > 0 else None
        # Here we would usually use Django forms to validate the input
        if not message:
            return CreateMessageMutation(
                status=400,
                formErrors=json.dumps(
                    {'message': ['Please enter a message.']}))
        obj = models.Message.objects.create(
            user=info.context.user, message=message, priority=priority            
        )
        return CreateMessageMutation(status=200, message=obj)


class Mutation(graphene.AbstractType):
    create_message = CreateMessageMutation.Field()
