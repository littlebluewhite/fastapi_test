import graphene
import uvicorn
from fastapi import FastAPI
from starlette.graphql import GraphQLApp


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        return "Hello " + name


app = FastAPI()
app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
