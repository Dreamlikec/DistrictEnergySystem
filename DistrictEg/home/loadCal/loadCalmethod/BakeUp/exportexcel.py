import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import xlsxwriter as xl


#打开文件
def Open_directory(title):
    
    try:
        #创建一个对话框
        application_window = tk.Tk()
        #去掉parant对话框
        application_window.withdraw()
        #得到打开文件夹的工作目录
        file_path = filedialog.askdirectory(parent = application_window,title = title)
    except Exception as e:
        file_path = None
        print (e)
    return file_path  
#将列表输出到excel,file_path为导出的路径，file_name为导出的文件名，output为导出的列表或者ndarray，heading为标题栏
def export_to_excel(file_path,file_name,output,heading):
    #创建一个workbook
    wb = xl.Workbook(file_path + '/{}.xlsx'.format(file_name))
    #创建一个worksheet
    sht = wb.add_worksheet('Sheet1')
    #将标题栏写入第一行
    sht.write_row('A1',heading)
    #如果查询结果不为空
    #将Mysql查询到的结果写入excel每一行
    for i in range(len(output)):
        sht.write_row('A'+str(i+2),output[i])
    wb.close()



