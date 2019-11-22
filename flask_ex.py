import os
from flask import Flask, render_template, jsonify, request, json , redirect, url_for
from flask_cors import CORS
from werkzeug import utils
import cx_Oracle

UPLOAD_FOLDER = './dist/static/image/tour_picture'
app = Flask(__name__,
            static_folder = "./static",
            template_folder = "./templates")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

USER = 'meenple'
PASS = 'meenple'
DB_URL = '10.10.100.65:1521/usfm'

@app.route('/hello')
def hello():
    try:
        con = cx_Oracle.connect(USER+'/'+PASS+'@'+DB_URL)
        return (con.version)
    finally:
        con.close()

@app.route('/test')
def hello2():
    return render_template('blank.html')

@app.route('/vendor')
def vendor():
    try:
        con = cx_Oracle.connect(USER+'/'+PASS+'@'+DB_URL)
        cur = con.cursor()
        sql = "select v.vendor_id, v.vendor_fname, v.vendor_lname, v.vendor_phone, "\
              "v.vendor_address, v.vendor_province, v.vendor_postcode "\
              "from vendor v"
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template('tables-vendor.html', rows=rows)
    finally:
        cur.close()
        con.close()

@app.route('/store')
def store():
    try:
        con = cx_Oracle.connect(USER+'/'+PASS+'@'+DB_URL)
        cur = con.cursor()
        sql = "select s.store_id, s.store_fname, s.store_lname, s.store_phone, "\
              "s.store_address, s.store_province, s.store_postcode "\
              "from store s"
        cur.execute(sql)
        rows = cur.fetchall()

        return render_template('tables-product.html',rows=rows)
    finally:
        cur.close()
        con.close()
    return render_template('tables-store.html')

@app.route('/product')
def product():
    try:
        con = cx_Oracle.connect(USER+'/'+PASS+'@'+DB_URL)
        cur = con.cursor()
        sql = "SELECT p.prod_id, p.prod_name, p.prod_weight, p.prod_details, p.prod_grouping "\
              "from product p"
        cur.execute(sql)
        rows = cur.fetchall()

        return render_template('tables-product.html',rows=rows)
    finally:
        cur.close()
        con.close()

@app.route('/shop')
def shop():
    try:
        con = cx_Oracle.connect(USER+'/'+PASS+'@'+DB_URL)
        cur = con.cursor()
        sql = "select v.vendor_id, v.vendor_fname, v.vendor_lname, v.vendor_phone, "\
              "v.vendor_province, p.prod_id, sp.prod_price, p.prod_name, p.prod_weight, "\
              "p.prod_details, p.prod_grouping "\
              "from vendor v "\
              "inner join sale_product sp "\
              "on v.vendor_id = sp.vendor_id "\
              "inner join product p "\
              "on p.prod_id = sp.prod_id"
        cur.execute(sql)
        rows = cur.fetchall()

        return render_template('tables-product.html',rows=rows)
    finally:
        cur.close()
        con.close()
    return render_template('tables-shop.html')

@app.route('/receipt')
def receipt():
    try:
        con = cx_Oracle.connect(USER+'/'+PASS+'@'+DB_URL)
        cur = con.cursor()
        sql = "select r.receipt_id, r.store_id, r.date_get, "\
              "po.id_po, po.date_po, rd.prod_id, rd.amount_receipt "\
              "from receipt r "\
              "inner join purchase_order po "\
              "on r.id_po = po.id_po "\
              "inner join receipt_detail rd "\
              "on rd.receipt_id = r.receipt_id"
        cur.execute(sql)
        rows = cur.fetchall()

        return render_template('tables-receipt.html',rows=rows)

    finally:
        cur.close()
        con.close()


@app.route('/order')
def order():
    try:
        con = cx_Oracle.connect(USER+'/'+PASS+'@'+DB_URL)
        cur = con.cursor()
        sql = "SELECT po.id_po, s.store_id, po.date_po, p.prod_id, pd.amount, "\
                "p.prod_name, p.prod_weight, p.prod_details, p.prod_grouping, s.store_fname, "\
                "s.store_lname, s.store_phone, s.store_province "\
                "FROM purchase_order po "\
                "inner join purchase_order_detail pd "\
                "on po.id_po = pd.id_po "\
                "inner join product p "\
                "on pd.prod_id = p.prod_id "\
                "inner join store s "\
                "on po.store_id = s.store_id"
        cur.execute(sql)
        rows = cur.fetchall()

        return render_template('tables-order.html',rows=rows)
    finally:
        cur.close()
        con.close()



@app.route('/invendor')
def vendor2():
    return render_template('insert-vendor.html')

@app.route('/invendor/post', methods=['POST'])
def vendor2_post():
    try:
        con = cx_Oracle.connect(USER + '/' + PASS + '@' + DB_URL)
        cur = con.cursor()
        sql = "INSERT INTO vendor ("\
              "vendor_id, "\
              "vendor_fname, "\
              "vendor_lname, "\
              "vendor_phone, "\
              "vendor_address, "\
              "vendor_province,"\
              "vendor_postcode "\
              ")VALUES ( "\
              "'"+request.form['InputID']+"', "\
              "'"+request.form['InputFirstName']+"', "\
              "'"+request.form['InputLastName']+"', "\
              "'"+request.form['InputPhone']+"', "\
              "'"+request.form['InputAddress']+"', "\
              "'"+request.form['InputProvince']+"', "\
              "'"+request.form['InputPostcode']+"' "\
              ")"
        print(sql)
        cur.execute(sql)
        con.commit()

        return render_template('insert-vendor.html')
    except cx_Oracle.DatabaseError as e:
        con.rollback()
    finally:
        cur.close()
        con.close()

@app.route('/upvendor')
def vendor3():
    return render_template('insert-vendor.html')

@app.route('/upvendor/post', methods=['POST'])
def vendor3_post():
    try:
        con = cx_Oracle.connect(USER + '/' + PASS + '@' + DB_URL)
        cur = con.cursor()
        sql = "UPDATE vendor "\
              "SET "\
              "vendor_fname = '"+request.form['InputFirstName']+"',  "\
              "vendor_lname = '"+request.form['InputLastName']+"', "\
              "vendor_phone = '"+request.form['InputPhone']+"', "\
              "vendor_address = '"+request.form['InputAddress']+"', "\
              "vendor_province = '"+request.form['InputProvince']+"', "\
              "vendor_postcode = '"+request.form['InputPostcode']+"' "\
              "WHERE "\
              "vendor_id = '"+request.form['InputID']+"' "
        print(sql)
        cur.execute(sql)
        con.commit()

        return render_template('insert-vendor.html')
    except cx_Oracle.DatabaseError as e:
        con.rollback()
    finally:
        cur.close()
        con.close()


@app.route('/instore')
def store2():
    return render_template('insert-store.html')

@app.route('/instore/post', methods=['POST'])
def store2_post():
    print(request.form['InputID'])
    print(request.form['InputFirstName'])
    print(request.form['InputLastName'])
    print(request.form['InputPhone'])
    print(request.form['InputAddress'])
    print(request.form['InputProvince'])
    print(request.form['InputPostcode'])
    return render_template('insert-store.html')

@app.route('/inproduct')
def product2():
    return render_template('insert-product.html')

@app.route('/inproduct/post', methods=['POST'])
def product2_post():
    print(request.form['InputID'])
    print(request.form['InputName'])
    print(request.form['InputLastWeight'])
    print(request.form['InputDetail'])
    print(request.form['InputGrouping'])
    return render_template('insert-product.html')

@app.route('/inshop')
def shop2():
    return render_template('insert-shop.html')

@app.route('/inshop/post', methods=['POST'])
def shop2_post():
    print(request.form['InputVendorID'])
    print(request.form['InputFirstName'])
    print(request.form['InputLastName'])
    print(request.form['InputPhone'])
    print(request.form['InputProvince'])
    print(request.form['InputProdID'])
    print(request.form['InputProdPrice'])
    print(request.form['InputProdName'])
    print(request.form['InputProdWeight'])
    print(request.form['InputProdDetail'])
    print(request.form['InputProdGrouping'])
    return render_template('insert-shop.html')

@app.route('/inreceipt')
def receipt2():
    return render_template('insert-receipt.html')

@app.route('/inreceipt/post', methods=['POST'])
def receipt2_post():
    print(request.form['InputReceiptID'])
    print(request.form['InputStoreID'])
    print(request.form['InputDateGet'])
    print(request.form['InputIDPO'])
    print(request.form['InputDatePO'])
    print(request.form['InputProdID'])
    print(request.form['InputAmountReceipt'])
    return render_template('insert-receipt.html')

@app.route('/inorder')
def order2():
    return render_template('insert-order.html')

@app.route('/inorder/post', methods=['POST'])
def order2_post():
    print(request.form['InputIDPO'])
    print(request.form['InputStoreID'])
    print(request.form['InputDatePO'])
    print(request.form['InputProdID'])
    print(request.form['InputAmount'])
    print(request.form['InputProdName'])
    print(request.form['InputProdWeight'])
    print(request.form['InputProdDetail'])
    print(request.form['InputProdGrouping'])
    print(request.form['InputStoreFirstName'])
    print(request.form['InputStoreLastName'])
    print(request.form['InputStorePhone'])
    print(request.form['InputStoreProvince'])
    return render_template('insert-order.html')


@app.route('/select')
def select():
    try:
        con = cx_Oracle.connect(USER+'/'+PASS+'@'+DB_URL)
        cur = con.cursor()
        sql = "select * from test1"
        cur.execute(sql)
        rows = cur.fetchall()
        for row in rows:
            print (row)
        return (con.version)
    finally:
        cur.close()
        con.close()

@app.route('/insert')
def insert():
    try:
        con = cx_Oracle.connect(USER+'/'+PASS+'@'+DB_URL)
        cur = con.cursor()
        data = {'ID':'01','NAME':'TEST'}
        sql = "insert into test1"   \
              "     (ID,"           \
              "     NAME)"          \
              "     values (       "\
              "'"+data['ID']+"',   "\
              "'"+data['NAME']+"'"  \
              ")"
        print(sql)
        cur.execute(sql)
        con.commit()
        return('True')
    except cx_Oracle.DatabaseError as e:
        con.rollback()
    finally:
        cur.close()
        con.close()

if __name__ == "__main__":
    # reload(sys)
    # sys.setdefaultencoding('utf-8')
    app.run(debug=True)
    # app.run(host = '0.0.0.0',port=5000)