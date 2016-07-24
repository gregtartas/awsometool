import sys, string, os, subprocess
from ctypes import *
from ctypes.wintypes import *
import difflib
from subprocess import CalledProcessError, check_output
import Tkinter
from Tkinter import *


# const variable
#=============================
TH32CS_SNAPPROCESS = 2
 
# struct
#=============================
class PROCESSENTRY32(Structure):
    _fields_ = [ ( 'dwSize' , DWORD ) ,
                 ( 'cntUsage' , DWORD) ,
                 ( 'th32ProcessID' , DWORD) ,
                 ( 'th32DefaultHeapID' , POINTER(ULONG)) ,
                 ( 'th32ModuleID' , DWORD) ,
                 ( 'cntThreads' , DWORD) ,
                 ( 'th32ParentProcessID' , DWORD) ,
                 ( 'pcPriClassBase' , LONG) ,
                 ( 'dwFlags' , DWORD) ,
                 ( 'szExeFile' , c_char * 260 ) ]
 
 
# forigen function
## CreateToolhelp32Snapshot
CreateToolhelp32Snapshot= windll.kernel32.CreateToolhelp32Snapshot
CreateToolhelp32Snapshot.reltype = c_long
CreateToolhelp32Snapshot.argtypes = [ c_int , c_int ]
 
## Process32First
Process32First = windll.kernel32.Process32First
Process32First.argtypes = [ c_void_p , POINTER( PROCESSENTRY32 ) ]
Process32First.rettype = c_int
 
## Process32Next
Process32Next = windll.kernel32.Process32Next
Process32Next.argtypes = [ c_void_p , POINTER(PROCESSENTRY32) ]
Process32Next.rettype = c_int
 
## CloseHandle
CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [ c_void_p ]
CloseHandle.rettype = c_int
 
#=======================================
class Window(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)               
		self.master = master
		self.init_window()

	def init_window(self):
		self.master.title("gui")
		self.pack(fill=BOTH, expand = 1)
		menu = Menu(self.master)
		self.master.config(menu=menu)
		file = Menu(menu)
		file.add_command(label = "Exit", command=self.client_exit)
		menu.add_cascade(label="File", menu=file)
		edit = Menu(menu)
		edit.add_command(label= "Show Text", command = self.showText)
		edit.add_command(label = "--help", command = self.help)
		edit.add_command(label= "poprawnosc", command = self.poprawnosc)
		menu.add_cascade(label="Edit", menu=edit)
	

	def showText(self):
		text = Label(self, text="nauka gui")
		text.pack()

	def client_exit(self):
		exit()
	
	def help(path):
		out = dumpOutput(r"C:/Users/gt/Desktop/AwesomeTool.exe --help")
		print (out)

	def poprawnosc (self):
		d = difflib.Differ()
		diff = d.compare(process, process2)
 
		f= open ('C:/Users/gt/Desktop/log-pl.txt', 'w')
		f.write ('+ / - shows differences in outputs \n')
		f.write ('\n'.join(diff))

		f.close()





def getProcessPid():
		hProcessSnap = 0
		hProcessSnap = CreateToolhelp32Snapshot( TH32CS_SNAPPROCESS , 0 )
 
		arr = []
		
		pe32 = PROCESSENTRY32()
		pe32.dwSize = sizeof( PROCESSENTRY32 )
       
		ret = Process32First( hProcessSnap , pointer( pe32 ) )
		while ret:
			arr.append( pe32.th32ProcessID )
			ret = Process32Next( hProcessSnap, pointer(pe32) )
			
		CloseHandle(hProcessSnap)
		
		return sorted(arr[1:])
		

def getProcessList():
		hProcessSnap = 0
		hProcessSnap = CreateToolhelp32Snapshot( TH32CS_SNAPPROCESS , 0 )
 
		arr = []
       
		pe32 = PROCESSENTRY32()
		pe32.dwSize = sizeof( PROCESSENTRY32 )
       
		ret = Process32First( hProcessSnap , pointer( pe32 ) )
		while ret:
			arr.append( pe32.szExeFile )
			ret = Process32Next( hProcessSnap, pointer(pe32) )
       
		CloseHandle(hProcessSnap)
		return sorted(arr[1:])
       
 
def dumpProcessOutput(processpath):
		out = check_output(processpath)
		out = out.replace('\r', '')
		arr = sorted(out.split('\n')[2:])
		return filter(None, arr)

def dumpOutput(path):
		out = check_output(path)
		print out

process2 = getProcessList()
print (process2)

process = dumpProcessOutput(r"C:/Users/gt/Desktop/AwesomeTool.exe -pl")
print (process)


#Compare AwsomeTool with Toolhelp32Snapshot
#=======================================


d = difflib.Differ()
diff = d.compare(process, process2)
 
f= open ('C:/Users/gt/Desktop/log-pl.txt', 'w')
f.write ('+ / - shows differences in outputs \n')
f.write ('\n'.join(diff))

f.close()

#sprawdzamy wynik nazwy procesu 
#==============================
"""
for proces in process: 
	wynik =  r'C:/Users/gt/Desktop/AwesomeTool.exe -pi --name ' + str(proces)
	processName = dumpProcessOutput (wynik) # process by name
	print processName
"""
#sprawdzamy wynik nazwy pid 
#==============================	
processPid = getProcessPid()

for pid in processPid: 
	wynik =  r'C:/Users/gt/Desktop/AwesomeTool.exe -pi --pid ' + str(pid)
	Pid = dumpOutput(wynik) # process by pid
	L=None
	if L is None:
		L = []
	L.append(Pid)
	L = str(L)
	L = L.replace ("Status: 5", "")
	print L[0]


#copyDirectory = dumpOutput (r"C:\Users\gt\Desktop\AwesomeTool.exe --cd") # copy directory
#print copyDirectory	

"""
#sprawdzamy
#==============================
try:
	
		
	#process2nd = dumpOutput(r"C:/Users/gt/Desktop/AwesomeTool.exe -pl -debug") #this process exit same data as process with arg -pl ?? 
	#print process2nd
	#hexDump = dumpOutput (r"C:/Users/gt/Desktop/AwesomeTool.exe -hex_dump C:/Users/gt/Desktop/python/plik.txt") # hexdump of given file <path> <offset> <lenght>
	#print hexDump
	#hexDump2 = dumpOutput (r"C:/Users/gt/Desktop/AwesomeTool.exe -hd")# jw
	#copyFile = dumpOutput (r"C:/Users/gt/Desktop/AwesomeTool.exe -cf C:/Users/gt/Desktop/python/plik.txt") # copy file
	
	forceCopy = dumpOutput (r"C:/Users/gt/Desktop/AwesomeTool.exe --force C:/Users/gt/Desktop/python/plik.txt") # force copy
	print (forceCopy)
	print (copyDirectory)

	#copyFile2 = dumpOutput (r"C:/Users/gt/Desktop/AwesomeTool.exe --copy_file C:/Users/gt/Desktop/python/plik.txt") # Copy file
	

except CalledProcessError as e:
	print(e.returncode)
	
#print processName
#print process
#print process2
#print process2nd  # same exit like arg -pl

"""
root = Tk()
root.geometry("400x400")
app = Window(root)
root.mainloop()
