@echo off

set API_URL=http://127.0.0.1:5000/add_employee
set DATA={"name": "John Doe", "position": "Software Engineer"}

rem Replace double quotes with escaped double quotes for JSON data
set DATA=%DATA:"=\"%

rem Send the POST request using curl with the data directly
curl -X POST -H "Content-Type: application/json" -d "%DATA%" %API_URL%
