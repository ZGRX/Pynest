from fastapi.testclient import TestClient
from app.main import app
from getpass import getpass
with TestClient(app) as client:
    response = client.get("/api/products/")
    print(response.status_code, response.json())

    email = input("邮箱：")
    password = getpass("密码：")
    login_response = client.post(
    "/api/auth/login",
    json={"email": email, "password": password},
    )
    print("登录状态码：", login_response.status_code)  

    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        print("登录成功，已取得 token")#取出登录返回的 token，供后面的请求使用。
        #创建一个库存为5的测试商品
        product_response = client.post(
            "/api/products/",
            json={"name": "测试商品", "description": "订单练习", "price": 30, "stock": 5},
            headers={"Authorization": f"Bearer {token}"},
        )#表示这是一个 格式化字符串（f-string）：字符串里的 {变量名} 会被替换成变量的值。
        print("创建商品：", product_response.status_code, product_response.json())
        #购买两件
        product_id = product_response.json()["id"]
        order_response = client.post(
            "/api/orders/",
            json={"product_id": product_id, "quantity": 2},
            headers={"Authorization": f"Bearer {token}"},
        )
        print("创建订单：", order_response.status_code, order_response.json())      
        #查询库存，确认是不是3
        product_after = client.get(f"/api/products/{product_id}")
        print("下单后库存：", product_after.json()["stock"])
        assert product_after.json()["stock"] == 3
        order_id = order_response.json()["id"]

        #取消刚刚创立的订单
        cancel_response = client.post(
            f"/api/orders/{order_id}/cancel",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert cancel_response.status_code == 200
        assert cancel_response.json()["status"] == "cancelled"
        product_stock = client.get(
            f"/api/products/{product_id}",
        )
        assert product_stock.json()["stock"] == 5

        #第二次取消刚刚的订单
        second_cancel_response = client.post(
           f"/api/orders/{order_id}/cancel",
            headers={"Authorization": f"Bearer {token}"},            
        )
        assert second_cancel_response.status_code == 400
        product_after_second_cancel = client.get(f"/api/products/{product_id}")
        assert product_after_second_cancel.json()["stock"] == 5
        print("重复取消检查通过")        
        #测试取消订单的支付
        pay_after_cancel_response = client.post(
            f"/api/orders/{order_id}/pay",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert pay_after_cancel_response.status_code == 400

        #测试新订单的支付
        product_id = product_response.json()["id"]
        order_response = client.post(
            "/api/orders/",
            json={"product_id": product_id, "quantity": 2},
            headers={"Authorization": f"Bearer {token}"},
        )
        new_order_id = order_response.json()["id"]
        print("创建订单：", order_response.status_code, order_response.json())              
        pay_response = client.post(
            f"/api/orders/{new_order_id}/pay",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert pay_response.json()["status"]== "paid"
        product_after_pay = client.get(f"/api/products/{product_id}")
        assert product_after_pay.json()["stock"] == 3

    else:
        print("登录失败：", login_response.json())
