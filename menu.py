'''
This class is for Menu
Threa are init(), build(), add(), save()
'''
import cx_Oracle as cx


class Menu:
    def display(self):
        conn = cx.connect("ora_user", "human123", "localhost/orcl")
        cur = conn.cursor()
        cur.execute("select menu, price, s_no from menu")
        for rec in cur:
            print('%2d %-12s %5d' % (rec[2], rec[0], rec[1]))
        conn.commit()
        cur.close()
        conn.close()

    def add(self):
        conn = cx.connect("ora_user", "human123", "localhost/orcl")
        cur = conn.cursor()
        name = input('새 메뉴명 ["":종료]: ')
        while name != '':
            price = int(input('새 가격:'))
            cur.execute(f"insert into menu (menu, price, s_no) values('{name}', {price}, snoseq.nextval)")
            name = input('새 메뉴명 ["":종료]: ')
        conn.commit()
        cur.close()
        conn.close()

    def delete(self):
        conn = cx.connect("ora_user", "human123", "localhost/orcl")
        cur = conn.cursor()
        num = input('삭제할 메뉴번호를 입력하시오 ["":종료] ')
        while num != '':
            cur.execute(f'delete from menu where s_no={num}')
            num = input('삭제할 메뉴번호를 입력하시오 ["":종료] ')
        conn.commit()
        cur.close()
        conn.close()

    def update(self):
        conn = cx.connect("ora_user", "human123", "localhost/orcl")
        cur = conn.cursor()
        num = input('수정할 메뉴번호를 입력하시오 ["":종료] ')
        while num != '':
            name = input('새 메뉴명을 입력하시오: ')
            price = int(input('가격을 입력하시오: '))
            cur.execute(f"update menu set menu='{name}', price={price} where s_no={num}")
            num = input('수정할 메뉴번호를 입력하시오 ["":종료] ')
        conn.commit()
        cur.close()
        conn.close()


class Order:
    count = 0

    def __init__(self):
        self.lOrder = []

    def add(self, oMenu):
        conn = cx.connect("ora_user", "human123", "localhost/orcl")  # DB연동
        cur = conn.cursor()
        cur2 = conn.cursor()
        name = ""
        price = ""
        oMenu.display()
        num = input('주문할 메뉴번호를 입력하시오 ["":종료] ')
        while num != '':
            cur2.execute(f"select menu, price from menu where s_no='{num}'")
            for rec in cur2:
                name = rec[0]
                price = rec[1]
            qty = input('주문할 수량을 입력하시오 ["":종료] ')
            if qty == "":
                break;

            self.count += 1

            print(f"주문번호: {self.count}")

            # 적립번호를 넣지 않고, 일괄적으로 마지막에 적립번호를 추가
            self.lOrder.append({'name': name,
                                'qty': int(qty),
                                'price': int(qty) * int(price),
                                'phone': ""})
            oMenu.display();
            num = input('주문할 메뉴번호를 입력하시오 ["":종료] ')

            # 일괄적으로 적립번호를 추가
        phone = input('적립번호를 입력하시오: ')
        for i in range(self.count):
            self.lOrder[i]['phone'] = phone
            cur.execute(f"insert into selling values(sysdate,"
                        f"'{self.lOrder[i]['phone']}',"
                        f"'{self.lOrder[i]['name']}',"
                        f"'{self.lOrder[i]['qty']}',"
                        f"'{self.lOrder[i]['price']}')")
        conn.commit()
        cur.close()
        cur2.close()
        conn.close()

    def display(self):
        total = 0;
        for i in range(self.count):
            print("수량: " + str(self.lOrder[i]['qty']))
            print("메뉴: " + self.lOrder[i]['name'])
            print("가격: " + str(self.lOrder[i]['price']))
            total += self.lOrder[i]['price']
        print('주문총액:%7d' % (total))


# This class is for Sales
class Sales:
    def __init__(self):
        self.lSales = []  # name, qty, price

    def display(self):
        total = 0;
        conn = cx.connect("ora_user", "human123", "localhost/orcl")
        cur = conn.cursor()
        cur.execute("select sell_time, mobile, name, qty, price from selling")
        for order in cur:
            print('%-12s %2d %6d %12s' % (order[2], order[3], order[4], order[1]))
            total += order[4]
        print('총매출액:%7d' % (total))
        str1 = '''

    This is string.
    String is a primitive data type.
    The limitation is not defined.
    '''

    def add(self, oOrder):
        for order in oOrder.lOrder:
            self.lSales.append(order)


gSales = Sales()
gMenu = Menu()  # Menu gMenu = new Menu();
job = input('작업을 선택하시오 [s:매출관리, o:주문관리, m:메뉴관리, "":종료] ')
while job != '':
    if job == 's':
        gSales.display()  # 매출전체리스트&총매출액 출력
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
    elif job == 'm':
        m_job = input('메뉴작업을 선택하시오 [a:추가, d:삭제, u:수정, l:목록, "":종료] ')
        while m_job != '':
            if m_job == 'a':
                gMenu.add()
            elif m_job == 'd':
                gMenu.delete()
            elif m_job == 'u':
                gMenu.update()
            elif m_job == 'l':
                gMenu.display()
            m_job = input('메뉴작업을 선택하시오 [a:추가, d:삭제, u:수정, l:목록, "":종료] ')
    job = input('작업을 선택하시오 [m:메뉴관리, o:주문관리, s:매출관리, "":종료] ')
print('프로그램 종료')