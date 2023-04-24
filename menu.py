'''
This class is for Menu
Threa are init(), build(), add(), save()
'''
class Menu:

  def __init__(self):
    self.lMenu =[]
    self.build()



  def build(self):
    f = open('d:/cafe/menu.txt', 'r')
    str = f.readline()
    while str != '':
      # print('str [' + str + ']')
      menu = str.split(',')
      dMenu = {'name': menu[0], 'price': int(menu[1])}
      self.lMenu.append(dMenu)
      str = f.readline()
    f.close()

  def save(self):
    f = open('d:/cafe/menu.txt', 'w')
    for menu in self.lMenu:
      line = menu['name'] + ',' + str(menu['price']) + '\n'
      f.write(line)
    f.close()

  def display(self):
    ndx=0
    for menu in self.lMenu:
      print('%2d %-12s %4d'%(ndx,menu['name'],menu['price']))
      ndx+=1

  def add(self):
    name = input('새 메뉴명 ["":종료]: ')
    while name != '':
      price = int(input('새 가격:'))
      self.lMenu.append({'name': name, 'price': price})
      name = input('새 메뉴명 ["":종료]: ')

  def delete(self):
    num = input('삭제할 메뉴번호를 입력하시오 ["":종료] ')
    while num != '':
      del self.lMenu[int(num)]
      num = input('삭제할 메뉴번호를 입력하시오 ["":종료] ')

  def update(self):
    num = input('삭제할 메뉴번호를 입력하시오 ["":종료] ')
    while num != '':
      name = input('새 메뉴명을 입력하시오')
      price = int(input('가격을 입력하시오'))
      self.lMenu[int(num)] = {'name': name, 'price': price}
      num = input('삭제할 메뉴번호를 입력하시오 ["":종료] ')


class Order:
  count = 0

  def __init__(self):
    self.lOrder = []

  def add(self, oMenu):
    oMenu.display()
    num = input('주문할 메뉴번호를 입력하시오 ["":종료] ')

    while num != '':
      qty = input('주문할 수량을 입력하시오 ["":종료] ')

      if qty == "":
        break;

      self.count += 1

      print(f"주문번호: {self.count}")

      # 적립번호를 넣지 않고, 일괄적으로 마지막에 적립번호를 추가
      self.lOrder.append({'name': oMenu.lMenu[int(num)]['name'],
                          'qty': int(qty),
                          'price': int(qty) * oMenu.lMenu[int(num)]['price'],
                          'phone': ""})
      oMenu.display();
      num = input('주문할 메뉴번호를 입력하시오 ["":종료] ')

      # 일괄적으로 적립번호를 추가
    phone = input('적립번호를 입력하시오: ')
    for i in range(self.count):
      self.lOrder[i]['phone'] = phone

  def display(self):
    total=0;
    for order in self.lOrder:
      print('%-12s %2d %6d'%(order['name'],order['qty'],order['price']))
      total+=order['price']
    print('주문총액:%7d'%(total))

# This class is for Sales
class Sales:
  def __init__(self):
    self.lSales=[] # name, qty, price

  def display(self):
    total=0
    for order in self.lSales:
      print('%-12s %2d %6d %12s'%(order['name'],order['qty'],order['price'],order['phone']))
      total+=order['price']
    print('총매출액: %d'%(total))
    str1='''
    This is string.
    String is a primitive data type.
    The limitation is not defined.
    '''

  def add(self,oOrder):
    for order in oOrder.lOrder:
      self.lSales.append(order)


gSales = Sales()
gMenu = Menu()     # Menu gMenu = new Menu();
job=input('작업을 선택하시오 [s:매출관리, o:주문관리, m:메뉴관리, "":종료] ')
while job!='':
  if job=='s':
    gSales.display() # 매출전체리스트&총매출액 출력
  elif job == 'o':
    gOrder = Order()
    m_job = input('주문작업을 선택하시오 [a:주문추가, l:주문내역, "":종료] ')
    while m_job != '':
      if m_job == 'a':
        gOrder.add(gMenu)
      elif m_job == 'l':
        gOrder.display()
      m_job = input('주문작업을 선택하시오 [a:주문추가, l:주문내역, "":종료] ')
    gSales.add(gOrder)
  elif job=='m':
    m_job =input('메뉴작업을 선택하시오 [a:추가, d:삭제, u:수정, l:목록, "":종료] ')
    while m_job!='' :
      if m_job=='a':
        gMenu.add()
      elif m_job=='d':
        gMenu.delete()
      elif m_job=='u':
        gMenu.update()
      elif m_job=='l':
        gMenu.display()
      m_job = input('메뉴작업을 선택하시오 [a:추가, d:삭제, u:수정, l:목록, "":종료] ')
    gMenu.save()
  job=input('작업을 선택하시오 [m:메뉴관리, o:주문관리, s:매출관리, "":종료] ')
print('프로그램 종료')
