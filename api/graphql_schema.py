import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import User as UserModel, HashResult as HashResultModel

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class HashResult(SQLAlchemyObjectType):
    class Meta:
        model = HashResultModel

class Query(graphene.ObjectType):
    all_users = graphene.List(User)
    all_hash_results = graphene.List(HashResult)

    def resolve_all_users(self, info):
        """Fetch all users from the database."""
        query = User.get_query(info)
        return query.all()

    def resolve_all_hash_results(self, info):
        """Fetch all hash results from the database."""
        query = HashResult.get_query(info)
        return query.all()

schema = graphene.Schema(query=Query)
