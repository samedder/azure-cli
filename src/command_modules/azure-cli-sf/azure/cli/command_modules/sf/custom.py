# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import sys
import urllib.parse
import requests

import azure.cli.core.azlogging as azlogging

from azure.cli.core._environment import get_config_dir
from azure.cli.core._config import AzConfig
from azure.cli.core.util import CLIError

# Really the CLI should do this for us but I cannot see how to get it to
CONFIG_PATH = os.path.join(get_config_dir(), "config")
az_config = AzConfig()

logger = azlogging.get_az_logger(__name__)

def sf_create_compose_application(application_name, file, repo_user=None,
                                  encrypted=False, repo_pass=None):
    # We need to read from a file which makes this a custom command
    # Encrypted param to indicate a password will be prompted
    """
    Creates a Service Fabric application from a Compose file

    :param str application_name:  The name of application to create from
    Compose file. This is typically the full name of the application
    including "fabric:" URI scheme
    :param str file: Path to the Compose file to use
    :param str repo_user: Container repository user name if needed for
    authentication
    :param bool encrypted: If true, indicate to use an encrypted password rather
    than prompting for a plaintext one
    :param str repo_pass: Encrypted container repository password
    """
    from azure.cli.core.util import read_file_content
    from azure.cli.command_modules.sf._factory import cf_sf_client
    from azure.cli.core.prompting import prompt_pass
    from azure.servicefabric.models.create_compose_application_description \
    import CreateComposeApplicationDescription
    from azure.servicefabric.models.repository_credential import RepositoryCredential

    if any([encrypted, repo_pass]) and not all([encrypted, repo_pass, repo_user]):
        raise CLIError("Invalid arguments: [ --application_name --file | \
        --application_name --file --repo_user | --application_name --file \
        --repo_user --encrypted --repo_pass ])")

    if repo_user:
        plaintext_pass = prompt_pass("Container repository password: ", False,
                                     "Password for container repository\
                                      containing container images")
        repo_pass = plaintext_pass

    repo_cred = RepositoryCredential(repo_user, repo_pass, encrypted)

    file_contents = read_file_content(file)

    model = CreateComposeApplicationDescription(application_name, file_contents, repo_cred)

    sf_client = cf_sf_client(None)
    sf_client.create_compose_application(model)

def sf_select(endpoint, cert=None, key=None, pem=None, ca=None):
    """
    Connects to a Service Fabric cluster endpoint.


    If connecting to secure cluster specify a cert (.crt) and key file (.key)
    or a single file with both (.pem). Do not specify both. Optionally, if
    connecting to a secure cluster, specify also a path to a CA bundle file
    or directory of trusted CA certs.

    :param str endpoint: Cluster endpoint URL, including port and HTTP or HTTPS prefix
    :param str cert: Path to a client certificate file
    :param str key: Path to client certificate key file
    :param str pem: Path to client certificate, as a .pem file
    :param str ca: Path to CA certs directory to treat as valid or CA bundle file
    """
    from azure.cli.core._config import set_global_config_value

    usage = "--endpoint [ [ --key --cert | --pem ] --ca ]"

    if ca and not (pem or all([key, cert])):
        raise CLIError("Invalid syntax: " + usage)

    if any([cert, key]) and not all([cert, key]):
        raise CLIError("Invalid syntax: " + usage)

    if pem and any([cert, key]):
        raise CLIError("Invalid syntax: " + usage)

    if pem:
        set_global_config_value("servicefabric", "pem_path", pem)
        set_global_config_value("servicefabric", "security", "pem")
    elif cert:
        set_global_config_value("servicefabric", "cert_path", cert)
        set_global_config_value("servicefabric", "key_path", key)
        set_global_config_value("servicefabric", "security", "cert")
    else:
        set_global_config_value("servicefabric", "security", "none")

    if ca:
        set_global_config_value("servicefabric", "ca_path", ca)

    set_global_config_value("servicefabric", "endpoint", endpoint)

def sf_get_ca_cert_info():
    az_config.config_parser.read(CONFIG_PATH)
    ca_cert = az_config.get("servicefabric", "ca_path", fallback=None)
    return ca_cert

def sf_get_connection_endpoint():
    az_config.config_parser.read(CONFIG_PATH)
    return az_config.get("servicefabric", "endpoint", fallback=None)

def sf_get_cert_info():
    az_config.config_parser.read(CONFIG_PATH)
    security_type = az_config.get("servicefabric", "security", fallback=None)
    if security_type is "pem":
        pem_path = az_config.get("servicefabric", "pem_path", fallback=None)
        return pem_path
    elif security_type is "cert":
        cert_path = az_config.get("servicefabric", "cert_path", fallback=None)
        key_path = az_config.get("servicefabric", "key_path", fallback=None)
        return cert_path, key_path
    elif security_type is "none":
        return None
    else:
        raise CLIError("Cluster security type not set")

    cert_path = az_config.get('servicefabric', 'cert_path', fallback=None)
    key_path = az_config.get('servicefabric', 'key_path', fallback=None)
    pem_path = az_config.get('servicefabric', 'pem_path', fallback=None)

    return (cert_path, key_path, pem_path)

class FileIter: # pylint: disable=too-few-public-methods
    def __init__(self, file, rel_file_path, print_progress):
        self.file = file
        self.rel_file_path = rel_file_path
        self.print_progress = print_progress

    def __iter__(self):
        return self

    def __next__(self):
        chunk = self.file.read(100000)
        if chunk == b'':
            raise StopIteration
        else:
            self.print_progress(len(chunk), self.rel_file_path)
            return chunk

def sf_copy_app_package(path):
    abspath = os.path.abspath(path)
    basename = os.path.basename(abspath)
    endpoint = sf_get_connection_endpoint()
    total_files_count = 0
    current_files_count = 0
    total_files_size = 0
    current_files_size = 0
    for root, _, files in os.walk(abspath):
        total_files_count += len(files)
        total_files_count += 1
        for file in files:
            t = os.stat(os.path.join(root, file))
            total_files_size += t.st_size

    def print_progress(size, rel_file_path):
        nonlocal current_files_size
        current_files_size += size
        sys.stdout.write("\r\033[K")
        print('[{}/{}] files, [{}/{}] bytes, {}'.format(current_files_count,
                                                        total_files_count,
                                                        current_files_size,
                                                        total_files_size,
                                                        rel_file_path),
              end="\r")
    for root, _, files in os.walk(abspath):
        rel_path = os.path.normpath(os.path.relpath(root, abspath))
        for file in files:
            url_path = os.path.normpath(os.path.join('ImageStore', basename,
                                                     rel_path, file)).replace('\\', '/')
            with open(os.path.normpath(os.path.join(root, file)), 'rb') as file_opened:
                url_parsed = list(urllib.parse.urlparse(endpoint))
                url_parsed[2] = url_path
                url_parsed[4] = urllib.parse.urlencode({'api-version': '3.0-preview'})
                url = urllib.parse.urlunparse(url_parsed)
                file_iter = FileIter(file_opened, os.path.normpath(
                    os.path.join(rel_path, file)), print_progress)
                _ = requests.put(url, data=file_iter)
                current_files_count += 1
                print_progress(0, os.path.normpath(os.path.join(rel_path, file)))
        url_path = os.path.normpath(os.path.join('ImageStore', basename,
                                                 rel_path, '_.dir')).replace('\\', '/')
        url_parsed = list(urllib.parse.urlparse(endpoint))
        url_parsed[2] = url_path
        url_parsed[4] = urllib.parse.urlencode({'api-version': '3.0-preview'})
        _ = requests.put(url)
        current_files_count += 1
        print_progress(0, os.path.normpath(os.path.join(rel_path, '_.dir')))
    sys.stdout.write("\r\033[K")
    print('[{}/{}] files, [{}/{}] bytes sent'.format(current_files_count,
                                                     total_files_count,
                                                     current_files_size,
                                                     total_files_size))

def sf_create_app(name, app_type, version, parameters=None, min_node_count=0, max_node_count=0, metrics=None):
    """
    Creates a Service Fabric application using the specified description.

    :param str name: Application name
    :param str app_type: Application type
    :param str version: Application version
    :param long min_node_count: The minimum number of nodes where Service Fabric
    will reserve capacity for this application. Note that this does not mean
    that the services of this application will be placed on all of those
    nodes.
    :param long max_node_count: The maximum number of nodes where Service Fabric
    will reserve capacity for this application. Note that this does not mean
    that the services of this application will be placed on all of those
    nodes.
    """
    from azure.servicefabric.models.application_description import ApplicationDescription
    from azure.servicefabric.models.application_parameter import ApplicationParameter
    from azure.servicefabric.models.application_capacity_description \
    import ApplicationCapacityDescription
    from azure.servicefabric.models.application_metric_description import \
    ApplicationMetricDescription
    from azure.cli.command_modules.sf._factory import cf_sf_client

    if min_node_count > max_node_count:
        raise CLIError("Note, the minimum node reserve capacity count cannot \
        be more than the maximum node count")

    app_params = None
    if parameters is not None:
        app_params = []
        for k in parameters:
            # Create an application parameter for every of these
            p = ApplicationParameter(k, parameters[k])
            app_params.append(p)

    # For simplicity, we assume user pass in valid key names in the list, or
    # ignore the input
    app_metrics = None
    if metrics is not None:
        app_metrics = []
        for k in metrics:
            metric = metrics[k]
            metric_name = metric.get("name", None)
            if metric_name is None:
                raise CLIError("Could not decode required application metric name")
            metric_max_cap = metric.get("maximum_capacity", 0)
            metric_reserve_cap = metric.get("reservation_capacity", 0)
            metric_total_cap = metric.get("total_application_capacity", 0)
            metric_desc = ApplicationMetricDescription(metric_name,
                                                       metric_max_cap,
                                                       metric_reserve_cap,
                                                       metric_total_cap)
            app_metrics.append(metric_desc)

    app_cap_desc = ApplicationCapacityDescription(min_node_count,
                                                  max_node_count,
                                                  app_metrics)

    app_desc = ApplicationDescription(name, app_type, version, app_params,
                                      app_cap_desc)

    sf_client = cf_sf_client(None)
    sf_client.create_application(app_desc)

def sf_upgrade_app(name, version, parameters, mode="UnmonitoredAuto", # pylint: disable=R0913
                   replica_set_check_timeout=None, force_restart=None,
                   failure_action=None, health_check_wait_duration=None,
                   health_check_stable_duration=None,
                   health_check_retry_timeout=None, upgrade_timeout=None,
                   upgrade_domain_timeout=None, warning_as_error=False,
                   max_unhealthy_apps=0, default_service_health_policy=None,
                   service_health_policy=None):
    """
    Starts upgrading an application in the Service Fabric cluster.

    Validates the supplied application upgrade parameters and starts upgrading
    the application if the parameters are valid.

    :param str name: Application name. The name of the target application,
    including the 'fabric' URI scheme.
    :param str version: The target application type version (found in the
    application manifest) for the application upgrade.
    :param str mode: The mode used to monitor health during a rolling upgrade.
    :param long replica_set_check_timeout: The maximum amount of time to block
    processing of an upgrade domain and prevent loss of availability when
    there are unexpected issues. Measured in seconds.
    :param bool force_restart: Forcefully restart processes during upgrade even
    when the code version has not changed.
    :param str failure_action: The action to perform when a Monitored upgrade
    encounters monitoring policy or health policy violations.
    :param int health_check_wait_duration: The amount of time to wait after
    completing an upgrade domain before applying health policies. Measured in
    milliseconds.
    :param int health_check_stable_duration: The amount of time that the
    application or cluster must remain healthy before the upgrade proceeds
    to the next upgrade domain. Measured in milliseconds.
    :param int health_check_retry_timeout: The amount of time to retry health
    evaluations when the application or cluster is unhealthy before the failure
    action is executed. Measured in milliseconds.
    :param int upgrade_timeout: The amount of time the overall upgrade has to
    complete before FailureAction is executed. Measured in milliseconds.
    :param int upgrade_domain_timeout: The amount of time each upgrade domain
    has to complete before FailureAction is executed. Measured in milliseconds.
    :param bool warning_as_error: Treat health evaluation warnings with the same
    severity as errors.
    :param int max_unhealthy_apps: The maximum allowed percentage of unhealthy
    deployed applications. Represented as a number between 0 and 100.
    """
    from azure.servicefabric.models.application_upgrade_description import \
    ApplicationUpgradeDescription
    from azure.servicefabric.models.application_parameter import \
    ApplicationParameter
    from azure.servicefabric.models.monitoring_policy_description import \
    MonitoringPolicyDescription
    from azure.servicefabric.models.application_health_policy import \
    ApplicationHealthPolicy
    from azure.servicefabric.models.service_type_health_policy import \
    ServiceTypeHealthPolicy
    from azure.servicefabric.models.service_type_health_policy_map_item import \
    ServiceTypeHealthPolicyMapItem
    from azure.cli.command_modules.sf._factory import cf_sf_client

    monitoring_policy = MonitoringPolicyDescription(failure_action,
                                                    health_check_wait_duration,
                                                    health_check_stable_duration,
                                                    health_check_retry_timeout,
                                                    upgrade_timeout,
                                                    upgrade_domain_timeout)

    app_params = None
    if parameters is not None:
        app_params = []
        for k in parameters:
            # Create an application parameter for every of these
            p = ApplicationParameter(k, parameters[k])
            app_params.append(p)

    def_shp = None
    if default_service_health_policy is not None:
        # Extract properties from dict using previously defined names
        shp = default_service_health_policy.get("max_percent_unhealthy_partitions_per_service", 0)
        rhp = default_service_health_policy.get("max_percent_unhealthy_replicas_per_partition", 0)
        ushp = default_service_health_policy.get("max_percent_unhealthy_services", 0)
        def_shp = ServiceTypeHealthPolicy(shp, rhp, ushp)

    map_shp = None
    if service_health_policy is not None:
        map_shp = []
        for st_desc in service_health_policy:
            st_name = st_desc.get("Key", None)
            if st_name is None:
                raise CLIError("Could not find service type name in service \
                               health policy map")
            st_policy = st_desc.get("Value", None)
            if st_policy is None:
                raise CLIError("Could not find service type policy in service \
                               health policy map")
            st_shp = st_policy.get("max_percent_unhealthy_partitions_per_service", 0)
            st_rhp = st_policy.get("max_percent_unhealthy_replicas_per_partition", 0)
            st_ushp = st_policy.get("max_percent_unhealthy_services", 0)

            std_policy = ServiceTypeHealthPolicy(st_shp, st_rhp, st_ushp)
            std_list_item = ServiceTypeHealthPolicyMapItem(st_name, std_policy)

            map_shp.append(std_list_item)

    app_health_policy = ApplicationHealthPolicy(warning_as_error,
                                                max_unhealthy_apps, def_shp,
                                                map_shp)

    desc = ApplicationUpgradeDescription(name, version, app_params, "Rolling",
                                         mode, replica_set_check_timeout,
                                         force_restart, monitoring_policy,
                                         app_health_policy)

    sf_client = cf_sf_client(None)
    sf_client.start_application_upgrade(name, desc)


    # TODO consider additional parameter validation here rather than allowing
    # the gateway to reject it and return failure response

def sf_create_service(app_name, name, type, singleton_scheme=False,
                      named_scheme=False, int_scheme=False,
                      named_scheme_list=None, int_scheme_low=None,
                      int_scheme_high=None, int_scheme_count=None,
                      constraints=None, correlated_service=None,
                      correlation=None, load_metrics=None, 
                      placement_policy_list=None, move_cost=None,
                      activation_mode=None, dns_name=None):
    """
    Creates the specified Service Fabric service from the description.

    :param str app_name: The identity of the parent application. This is
    typically the full name of the application without the 'fabric:' URI scheme.
    :param str name: Name of the service.
    :param str type: Name of the service type.
    :param bool singleton_scheme: Indicates the service should have a single
    partition or be a non-partitioned service.
    :param bool named_scheme: Indicates the service should have multiple named
    partitions.
    :param list of str named_scheme_list: The list of names to partition the
    service across, if using the named partition scheme.
    :param bool int_scheme: Indicates the service should be uniformly
    partitioned across a range of unsigned integers.
    :param str int_scheme_low: The start of the key integer range, if using an
    uniform integer partition scheme.
    :param str int_scheme_high: The end of the key integer range, if using an
    uniform integer partition scheme.
    :param str int_scheme_count: The number of partitions inside the integer
    key range to create, if using an uniform integer partition scheme.
    :param str constraints: The placement constraints as a string. Placement
    constraints are boolean expressions on node properties and allow for
    restricting a service to particular nodes based on the service requirements.
    For example, to place a service on nodes where NodeType is blue specify the
    following:"NodeColor == blue".
    :param str correlation: Correlate the service with an existing service
    using an alignment affinity. Possible values include: 'Invalid', 'Affinity',
    'AlignedAffinity', 'NonAlignedAffinity'.
    :param str correlated_service: Name of the target service to correlate with.
    :param str move_cost: Specifies the move cost for the service. Possible 
    values are: 'Zero', 'Low', 'Medium', 'High'.
    :param str activation_mode: The activation mode for the service package.
    Possible values include: 'SharedProcess', 'ExclusiveProcess'.
    :param str dns_name: The DNS name of the service to be created. The Service
    Fabric DNS system service must be enabled for this setting.
    """
    from azure.servicefabric.models.service_description import ServiceDescription
    from azure.servicefabric.models.named_partition_scheme_description \
    import NamedPartitionSchemeDescription
    from azure.servicefabric.models.singleton_partition_scheme_description \
    import SingletonPartitionSchemeDescription
    from azure.servicefabric.models.uniform_int64_range_partition_scheme_description \
    import UniformInt64RangePartitionSchemeDescription
    from azure.servicefabric.models.service_correlation_description \
    import ServiceCorrelationDescription
    from azure.servicefabric.models.service_load_metric_description \
    import ServiceLoadMetricDescription
    from azure.servicefabric.models.service_placement_non_partially_place_service_policy_description \
    import ServicePlacementNonPartiallyPlaceServicePolicyDescription
    from azure.servicefabric.models.service_placement_prefer_primary_domain_policy_description \
    import ServicePlacementPreferPrimaryDomainPolicyDescription
    from azure.servicefabric.models.service_placement_required_domain_policy_description \
    import ServicePlacementRequiredDomainPolicyDescription
    from azure.servicefabric.models.service_placement_require_domain_distribution_policy_description \
    import ServicePlacementRequireDomainDistributionPolicyDescription
    from azure.cli.command_modules.sf._factory import cf_sf_client

    if sum([singleton_scheme, named_scheme, int_scheme]) is not 1:
        raise CLIError("Specify exactly one partition scheme")

    part_schema = None
    if singleton_scheme:
        part_schema = SingletonPartitionSchemeDescription()
    elif named_scheme:
        if not named_scheme_list:
            raise CLIError("When specifying named partition scheme, must \
            include list of names")
        part_schema = NamedPartitionSchemeDescription(len(named_scheme_list), named_scheme_list)
    elif int_scheme:
        if not all([int_scheme_low, int_scheme_high, int_scheme_count]):
            raise CLIError("Must specify the full integer range and partition \
            count when using an uniform integer partition scheme")
        part_schema = UniformInt64RangePartitionSchemeDescription(int_scheme_count,
                                                                  int_scheme_low,
                                                                  int_scheme_high)

    corre = None
    if any([correlated_service, correlation]):
        if not all([correlated_service, correlation]):
            raise CLIError("Must specify both a correlation service and \
            correlation scheme")
        corre = ServiceCorrelationDescription(correlation, correlated_service)

    load_list = None
    if load_metrics is not None:
        load_list = []
        for l in load_metrics:
            l_name = l.get("name", None)
            if l_name is None:
                raise CLIError("Could not find specified load metric name")
            l_weight = l.get("weight", None)
            l_primary = l.get("primary_default_load", None)
            l_secondary = l.get("secondary_default_load", None)
            l_default = l.get("default_load", None)
            l_desc = ServiceLoadMetricDescription(l_name, l_weight, l_primary,
                                                  l_secondary, l_default)
            load_list.append(l_desc)

    place_policy = None
    if placement_policy_list:
        place_policy = []
        valid_policies = [
            "NonPartiallyPlaceService",
            "PreferPrimaryDomain",
            "RequireDomain",
            "RequireDomainDistribution"
        ]
        # Not entirely documented but similar to the property names
        for p in placement_policy_list:
            p_type = p.get("type", None)
            if p_type is None:
                raise CLIError("Could not determine type of specified \
                placement policy")
            if p_type not in valid_policies:
                raise CLIError("Invalid type of placement policy specified")
            p_domain_name = p.get("domain_name", None)
            if (p_domain_name is None) and (p_type != "NonPartiallyPlaceService"):
                raise CLIError("Placement policy type requires target domain \
                name")
            if p_type == "NonPartiallyPlaceService":
                p_policy = ServicePlacementNonPartiallyPlaceServicePolicyDescription()
            elif p_type == "PreferPrimaryDomain":
                p_policy = ServicePlacementPreferPrimaryDomainPolicyDescription(p_domain_name)
            elif p_type == "RequireDomain":
                p_policy = ServicePlacementRequiredDomainPolicyDescription(p_domain_name)
            elif p_type == "RequireDomainDistribution":
                p_policy = ServicePlacementRequireDomainDistributionPolicyDescription(p_domain_name)
            place_policy.append(p_policy)

    # API weirdness where we both have to specify a move cost, and a indicate
    # the existence of a default move cost
    move_cost_specified = None
    if move_cost is not None:
        valid_costs = [
            "Zero",
            "Low",
            "Medium",
            "High"
        ]
        if move_cost not in valid_costs:
            raise CLIError("Invalid move cost specified")
        move_cost_specified = True

    if activation_mode is not None:
        valid_modes = [
            "SharedProcess",
            "ExclusiveProcess"
        ]
        if activation_mode not in valid_modes:
            raise CLIError("Invalid activation mode specified")

    sd = ServiceDescription(name, type, part_schema, app_name, None,
                            constraints, corre, load_list, place_policy,
                            move_cost, move_cost_specified, activation_mode,
                            dns_name)

    sf_client = cf_sf_client(None)
    sf_client.create_service(app_name, sd)
