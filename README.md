create folder like
File-integrity-moniter/
|
|---integrity.py
|---moniter.py
|---report.py
|---main.py
|
|
|--------baseline/
|--------logs/ 
|--------reports/
|--------test_files/

then upload requests requirements:
pip -r intall requirements.txt


create a file in test_file:
echo "Modified configuration" > test_files/config.txt  

then to run file :
python3 main.py init --directory test_files 

modify the file te check:
echo "Original security configuration" > test_files/config.txt  

then check the test file::
 python main.py check --directory test_files 

 


