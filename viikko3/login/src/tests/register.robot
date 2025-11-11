*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  liisa
    Set Password  liisa123
    Set Password Confirmation  liisa123
    Click Button  Register
    Welcome Page Should Be Open

Register With Too Short Username And Valid Password
    Set Username  li
    Set Password  liisa123
    Set Password Confirmation  liisa123
    Click Button  Register
    Register Page Should Be Open
    Registration Should Fail With Message  Username should be at leats 3 characters long

Register With Valid Username And Too Short Password
    Set Username  liisa
    Set Password  li
    Set Password Confirmation  li
    Click Button  Register
    Register Page Should Be Open
    Registration Should Fail With Message  Password should be at least 8 characters long

Register With Valid Username And Invalid Password
    Set Username  liisa
    Set Password  liisaliisa
    Set Password Confirmation  liisaliisa
    Click Button  Register
    Register Page Should Be Open
    Registration Should Fail With Message  Password should contain at least one other character than letters

Register With Nonmatching Password And Password Confirmation
    Set Username  liisa
    Set Password  liisa123
    Set Password Confirmation  liisa321
    Click Button  Register
    Register Page Should Be Open
    Registration Should Fail With Message  Password and password confirmation do not match

Register With Username That Is Already In Use
    Set Username  pekka
    Set Password  pekka123
    Set Password Confirmation  pekka123
    Click Button  Register
    Register Page Should Be Open
    Registration Should Fail With Message  Username already in use

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  pekka  pekka123
    Go To  ${REGISTER_URL}

Set Password Confirmation
    [Arguments]  ${password}
    Input Password  password_confirmation  ${password}

Registration Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}
