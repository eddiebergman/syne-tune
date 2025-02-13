# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
from typing import Dict, Any, Optional
import logging

from syne_tune.experiments import ComparativeResults, PlotParameters
from syne_tune.experiments.multiobjective import hypervolume_indicator_column_generator
from benchmarking.nursery.benchmark_multiobjective.baselines import methods
from benchmarking.nursery.benchmark_multiobjective.benchmark_definitions import (
    benchmark_definitions,
)


def metadata_to_setup(metadata: Dict[str, Any]) -> Optional[str]:
    # The setup is the algorithm. No filtering
    return metadata["algorithm"]


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    experiment_name = "icml-17"
    experiment_names = (experiment_name,)
    setups = list(methods.keys())
    num_runs = 20
    download_from_s3 = False  # Set ``True`` in order to download files from S3
    # Plot parameters across all benchmarks
    plot_params = PlotParameters(
        xlabel="wall-clock time",
        aggregate_mode="iqm_bootstrap",
        grid=True,
    )
    # The creation of ``results`` downloads files from S3 (only if
    # ``download_from_s3 == True``), reads the metadata and creates an inverse
    # index. If any result files are missing, or there are too many of them,
    # warning messages are printed
    results = ComparativeResults(
        experiment_names=experiment_names,
        setups=setups,
        num_runs=num_runs,
        metadata_to_setup=metadata_to_setup,
        plot_params=plot_params,
        download_from_s3=download_from_s3,
    )

    # We can now create plots for the different benchmarks
    # First: nas201-mo-cifar100
    benchmark_name = "nas201-mo-cifar100"
    benchmark = benchmark_definitions[benchmark_name]
    # We would like to plot the hypervolume indicator, which is a derived
    # metric
    dataframe_column_generator = hypervolume_indicator_column_generator(
        metrics_and_modes=list(zip(benchmark.metric, benchmark.mode))
    )
    plot_params = PlotParameters(
        metric="hypervolume_indicator",
        mode="max",
        convert_to_min=False,
    )
    results.plot(
        benchmark_name=benchmark_name,
        plot_params=plot_params,
        dataframe_column_generator=dataframe_column_generator,
        one_result_per_trial=True,
        file_name=f"./{experiment_name}-{benchmark_name}.png",
    )
    # Next: nas201-mo-ImageNet16-120
    benchmark_name = "nas201-mo-ImageNet16-120"
    benchmark = benchmark_definitions[benchmark_name]
    dataframe_column_generator = hypervolume_indicator_column_generator(
        metrics_and_modes=list(zip(benchmark.metric, benchmark.mode))
    )
    results.plot(
        benchmark_name=benchmark_name,
        plot_params=plot_params,
        dataframe_column_generator=dataframe_column_generator,
        one_result_per_trial=True,
        file_name=f"./{experiment_name}-{benchmark_name}.png",
    )
