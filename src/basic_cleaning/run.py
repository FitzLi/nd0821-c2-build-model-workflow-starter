#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    ######################
    # YOUR CODE HERE     #
    ######################
    # Select obs that have non-outlier price
    idx = df['price'].between(args.min_price, args.max_price) & \
            df['longitude'].between(-74.25, -73.50) & \
            df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()
    # Covert 'last_review' to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    # Save the cleaned data
    df.to_csv(args.output_artifact, index=False)
    
    # Create and upload the artifact to W&B
    artifact = wandb.Artifact(
            name=args.output_artifact,
            type=args.output_type,
            description=args.output_description
        )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact",
        type=str,
        help="The name of the raw data artifact that should be loaded",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="The name of the cleaned data artifact that will be loaded to W&B",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="The type of the cleaned data artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="The description of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="The minimum non-outlier price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="The maximum non-outlier price",
        required=True
    )

    args = parser.parse_args()

    go(args)
