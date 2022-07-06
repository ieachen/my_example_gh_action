from pathlib import Path
import fitz
import PySimpleGUI as sg


def pdf_save_each_page_to_picture(pdf_file_path, output_pic_folder):

    pdf_file_path = Path(pdf_file_path)
    output_pic_folder = Path(output_pic_folder)

    # 要求路径存在
    if not pdf_file_path.exists():
        print('pdf路径不正确，请重试')
        return
    if not output_pic_folder.exists():
        print('图片保存目录不存在，请重试')
        return

    # 要求路径以 .pdf 结尾
    if not str(pdf_file_path).endswith('.pdf'):
        print('pdf路径不是以 .pdf 结尾，请重试')
        return

    print('\n --------- pdf 保存每一页为图片 -------\n')

    print('pdf 路径： ' + str(pdf_file_path))
    print('图片保存目录： ' + str(output_pic_folder))

    pdf_name_with_no_extension = pdf_file_path.name.split('.')[0]

    doc = fitz.open(pdf_file_path)  # 打开pdf

    total_page_number = doc.page_count  # 总页数，或者len(doc)
    total_page_number_digit = len(str(total_page_number))  # 总页数是几位数字，用于 zfill

    for ii in range(doc.page_count):  # 或者直接 for page in doc:
        print(f'  保存图片：第 {ii} 页')

        ii_str = str(ii).zfill(total_page_number_digit)  # zfill的目的为了在文件管理器里排序正常

        output_file_path = output_pic_folder /  f"{pdf_name_with_no_extension}_{ii_str}.png"

        page = doc.load_page(ii)
        pix = page.get_pixmap()
        pix.save(output_file_path)

    doc.close()

    print('\n 完成！')

    return


def main():

    # sg.theme('DarkAmber')  # 设置当前主题

    # 界面布局，将会按照列表顺序从上往下依次排列，二级列表中，从左往右依此排列
    layout = [
        [sg.Text('pdf 保存每一页为图片', justification='center')],

        [sg.Text('-----------------')], 

        [sg.Text('步骤1. 选择 pdf 文件：')],  # T = Text
        [sg.InputText(key='pdf_file', visible=True)],  # InputText = Input = In = I
        [sg.FileBrowse(key='_BUTTON_KEY_', target='pdf_file', file_types=[('pdf files', '*.pdf')])],

        [sg.Text('-----------------')], 

        [sg.Text('步骤2. 选择图片保存目录（最好是空目录）：')], 
        [sg.InputText(key='pic_folder', visible=True)],  # InputText = Input = In = I
        [sg.FolderBrowse(key='_BUTTON_KEY2_', target='pic_folder')],


        [sg.Text('-----------------')], 

        # [sg.Text('你选择的文件夹是:',font=("宋体", 10)),sg.Text('',key='pic_folder',size=(50,1),font=("宋体", 10))],

        [sg.Text('步骤3. 点击“开始”按钮')], 
        [sg.Button('开始', tooltip='执行pdf转图片'), sg.Button('取消', tooltip='关闭'), sg.Button('清空', tooltip='清空文件选择')],

        [sg.Output(size=(60, 15))]

        # [sg.Text('Some text on Row 1')],
        # [sg.Text('Enter something on Row 2'), sg.InputText()],

        # [sg.FolderBrowse(key='_BUTTON_KEY_', target='input_folder'), sg.OK()],
    ]

    # 创造窗口
    window = sg.Window('pdf 保存为每一页图片', layout)
    # 事件循环并获取输入值

    while True:
        event, values = window.read()
        if event in (None, '取消'):  # 如果用户关闭窗口或点击`Cancel`
            break

        # print(event)
        # print(values)

        if event == '开始':
            if values['pdf_file'] and values['pic_folder']:
                pdf_save_each_page_to_picture(values['pdf_file'], values['pic_folder'])

        if event == '清空':
            window['pdf_file'].Update('')
            window['pic_folder'].Update('')

        # if event == '重命名':
        #     if values['folder']:
        #         print('{0}正在重命名原文件为hash值{0}'.format('*'*10))
        #         mult_rename(values['folder'])
        #         print('{0}重命名完毕{0}'.format('*'*10))
        #     else:
        #         print('请先选择文件夹')

        # print('You entered ', values[0])

    window.close()


if __name__ == '__main__':
    main()

