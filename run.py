from nornir import InitNornir
from nornir_utils.plugins.functions.print_result import print_result
from nornir_scrapli.tasks import netconf_get, netconf_edit_config, netconf_capabilities
from nornir_napalm.plugins.tasks import napalm_cli
from nornir_jinja2.plugins.tasks import template_file

nr = InitNornir(config_file="nornir_data/config.yaml")

for host in nr.inventory.hosts.keys():
    nr_result = nr.run(task=netconf_capabilities,
                        name='Get NETCONF Capabilities')[host][0]
    # Check to make sure app hosting is a valid capability
    assert any('Cisco-IOS-XE-app-hosting-oper' in i for i in nr_result.result)
    assert any('Cisco-IOS-XE-app-hosting-cfg' in i for i in nr_result.result)
    # Render config RPC with vars from inventory
    rpc_tmpl_result = nr.run(task=template_file,
            name='RPC Template Processing',
            template='app_hosting_cfg.xml.j2',
            path='rpc_templates/',
            **nr.inventory.groups['global'].data
            )
    ah_cfg = rpc_tmpl_result[host].result
    # Send config RPC with App Hosting configuration
    cfg_result = nr.run(task=netconf_edit_config, config=ah_cfg)
    print_result(cfg_result)
    # Run the install exec command
    # Looking for exec commands via Netconf
    install_cmd = 'app-hosting install appid 1keyes package https://downloads.thousandeyes.com/enterprise-agent/thousandeyes-enterprise-agent-3.0.cat9k.tar'
    install_result = nr.run(task=napalm_cli, commands=[install_cmd])
    print_result(install_result)
    # Get App Hosting Netconf filter
    with open('rpc_templates/app_hosting_oper.xml') as fh:
        ncfilter = fh.read()
    # Get App Hosting configuration RPC
    ah_result = nr.run(task=netconf_get, filter_=ncfilter)
    print_result(ah_result)