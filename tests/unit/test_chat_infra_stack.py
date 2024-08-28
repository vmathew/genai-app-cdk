import aws_cdk as core
import aws_cdk.assertions as assertions

from chat_infra.chat_infra_stack import ChatInfraStack

# example tests. To run these tests, uncomment this file along with the example
# resource in chat_infra/chat_infra_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ChatInfraStack(app, "chat-infra")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
