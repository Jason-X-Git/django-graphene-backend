import graphene
import simple_app.schema


class Queries(
    simple_app.schema.Query,
    graphene.ObjectType
):
    dummy = graphene.String()

    def resolve_dummy(self, context, **kwargs):
        return 'I am super star !'


class Mutations(
    simple_app.schema.Mutation,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Queries, mutation=Mutations)
