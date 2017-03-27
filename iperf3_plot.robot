*** Settings ***
Documentation    Suite description
Library          iperf3_plot_library.py
Library           Collections


*** Test Cases ***
Test Parse Parameters -f, -o from cmd
    [Tags]    DEBUG
    Set Test Variable   ${foldername}   ./testTarball
    Set Test Variable   ${plotFiles}    []
    Set Test Variable   ${noPlotFiles}  []
    Set Test Variable   ${output}       graph/all.png
    Set Test Variable   ${upperLimit}   0
    Set Test Variable   ${lowerLimit}   0
    Set Test Variable   ${bound}        []

    parse_option_from_cmd   -f   ${foldername}   -o  ${output}
    print_message   foldername ${foldername}\n plotFiles ${plotFiles}\n noPlotFiles ${noPlotFiles}\n output ${output}\n upperLimit ${upperLimit}\n lowerLimit ${lowerLimit}\n bound ${bound}

Test Parameters -f, -o
    [Tags]    DEBUG

    Set Test Variable   ${foldername}   ./testTarball
    Set Test Variable   ${plotFiles}    []
    Set Test Variable   ${noPlotFiles}  []
    Set Test Variable   ${output}       graph/all.png
    Set Test Variable   ${upperLimit}   0
    Set Test Variable   ${lowerLimit}   0
    Set Test Variable   ${bound}        []

    parse_options   -f   ${foldername}   -o  ${output}
    Result should be    ${foldername}   ${plotFiles}   ${noPlotFiles}    ${output}   ${upperLimit}   ${lowerLimit}    ${bound}
    print_message   foldername ${foldername}\n plotFiles ${plotFiles}\n noPlotFiles ${noPlotFiles}\n output ${output}\n upperLimit ${upperLimit}\n lowerLimit ${lowerLimit}\n bound ${bound}

Test Parameters -f, -o, -b, -u, -l
    [Tags]    DEBUG

    Set Test Variable   ${foldername}   ./testTarball
    Set Test Variable   ${plotFiles}    []
    Set Test Variable   ${noPlotFiles}  []
    Set Test Variable   ${output}       graph/all.png
    Set Test Variable   ${upperLimit}   0.5
    Set Test Variable   ${lowerLimit}   0.45
    Set Test Variable   ${bound}        [0.42,0.42,0.42M],[0.46,0.46,0.46M]
    Set Test Variable   ${expbound}     [[0.42, 0.42, '0.42M'], [0.46, 0.46, '0.46M']]

    parse_options   -f  ${foldername}   -o  ${output}   -b ${bound}  -u ${upperLimit}   -l ${lowerLimit}
    Result should be    ${foldername}   ${plotFiles}   ${noPlotFiles}    ${output}   ${upperLimit}   ${lowerLimit}    ${expbound}
    print_message   foldername ${foldername}\n plotFiles ${plotFiles}\n noPlotFiles ${noPlotFiles}\n output ${output}\n upperLimit ${upperLimit}\n lowerLimit ${lowerLimit}\n bound ${expbound}


Test Parameters -f, -o, -p
    [Tags]    DEBUG

    Set Test Variable   ${foldername}   ./testTarball
    Set Test Variable   ${plotFiles}    tg_server_00004,tg_server_00009
    Set Test Variable   ${expplotFiles}     ['tg_server_00004', 'tg_server_00009']
    Set Test Variable   ${noPlotFiles}  []
    Set Test Variable   ${output}       graph/s49_bound.png
    Set Test Variable   ${upperLimit}   0
    Set Test Variable   ${lowerLimit}   0
    Set Test Variable   ${bound}        []
    Set Test Variable   ${expbound}     []


    parse_options   -f  ${foldername}   -o  ${output}   -p ${plotFiles}
    Result should be    ${foldername}   ${expplotFiles}   ${noplotFiles}    ${output}   ${upperLimit}   ${lowerLimit}    ${expbound}
    print_message   foldername ${foldername}\n plotFiles ${expplotFiles}\n noPlotFiles ${noPlotFiles}\n output ${output}\n upperLimit ${upperLimit}\n lowerLimit ${lowerLimit}\n bound ${expbound}

Test Parameters -f, -o, -p, -u, -l
    [Tags]    DEBUG

    Set Test Variable   ${foldername}   ./testTarball
    Set Test Variable   ${plotFiles}    tg_server_00004,tg_server_00009
    Set Test Variable   ${expplotFiles}     ['tg_server_00004', 'tg_server_00009']
    Set Test Variable   ${noPlotFiles}  []
    Set Test Variable   ${output}       graph/s49_bound.png
    Set Test Variable   ${upperLimit}   0.5
    Set Test Variable   ${lowerLimit}   0.45
    Set Test Variable   ${bound}        []
    Set Test Variable   ${expbound}     []

    parse_options   -f  ${foldername}   -o  ${output}   -p ${plotFiles}  -u  ${upperLimit}  -l    ${lowerLimit}
    Result should be    ${foldername}   ${expplotFiles}   ${noplotFiles}    ${output}   ${upperLimit}   ${lowerLimit}    ${expbound}
    print_message   foldername ${foldername}\n plotFiles ${expplotFiles}\n noPlotFiles ${noPlotFiles}\n output ${output}\n upperLimit ${upperLimit}\n lowerLimit ${lowerLimit}\n bound ${expbound}

Test Parameters -f, -o, -n
    [Tags]    DEBUG
    Set Test Variable   ${foldername}       ./testTarball
    Set Test Variable   ${plotFiles}        []
    Set Test Variable   ${expplotFiles}     []
    Set Test Variable   ${noPlotFiles}       tg_server_00004,tg_server_00009
    Set Test Variable   ${expNoPlotFiles}    ['tg_server_00004', 'tg_server_00009']
    Set Test Variable   ${output}           graph/s49_bound.png
    Set Test Variable   ${upperLimit}       0
    Set Test Variable   ${lowerLimit}       0
    Set Test Variable   ${bound}            []
    Set Test Variable   ${expbound}         []

    parse_options   -f  ${foldername}   -o  ${output}   -n ${noPlotFiles}
    Result should be    ${foldername}   ${expplotFiles}   ${expNoplotFiles}    ${output}   ${upperLimit}   ${lowerLimit}    ${expbound}
    print_message   foldername ${foldername}\n plotFiles ${expplotFiles}\n noPlotFiles ${expNoPlotFiles}\n output ${output}\n upperLimit ${upperLimit}\n lowerLimit ${lowerLimit}\n bound ${expbound}

