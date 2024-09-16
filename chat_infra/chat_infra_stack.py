from aws_cdk import (
    CfnOutput,
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets,
    aws_ec2 as ec2,
    aws_iam as iam
)
from constructs import Construct

class ChatInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, "AppVPC", max_azs=2)

        cluster = ecs.Cluster(self, "AppCluster", vpc=vpc)

        task_definition = ecs.FargateTaskDefinition(
            self,
            "AppTaskDef",
            memory_limit_mib=2048,
            cpu=1024,
            runtime_platform=ecs.RuntimePlatform(
                cpu_architecture=ecs.CpuArchitecture.ARM64,
                operating_system_family=ecs.OperatingSystemFamily.LINUX
            )
        )

        container = task_definition.add_container(
            "StreamlitContainer",
            image=ecs.ContainerImage.from_asset("./app", 
                platform=ecr_assets.Platform.LINUX_ARM64),
            environment={
                "STREAMLIT_SERVER_PORT": "8501",
                "STREAMLIT_SERVER_ADDRESS": "0.0.0.0"
            },
            logging=ecs.LogDrivers.aws_logs(stream_prefix="StreamlitContainer")
        )

        container.add_port_mappings(ecs.PortMapping(container_port=8501))

        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "StreamlitService",
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True,
            listener_port=80
        )

        fargate_service.task_definition.add_to_task_role_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:ListFoundationModels"
                ],
                resources=["*"]
            )
        )

        CfnOutput(
            self,
            "LoadBalancerDNS",
            value=fargate_service.load_balancer.load_balancer_dns_name,
            description="Load Balancer DNS Name"
        )

