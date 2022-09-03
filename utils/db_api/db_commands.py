from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from environs import Env
env = Env()
env.read_env()


DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")

class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            database=DB_NAME,
        )
        
    async def execute(
        self,
        command,
        *args,
        fetch: bool = False,
        fetchval: bool = False,
        fetchrow: bool = False,
        execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result
        
    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)
        
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
        
    
    
    
    
    
    
    async def create_table_products(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Products (
        id SERIAL PRIMARY KEY,
        category_name VARCHAR(50) NOT NULL,
        productname VARCHAR(50) NOT NULL,
        photo varchar(255) NULL,
        price INT NOT NULL, 
        description VARCHAR(3000) NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_product(
        self,
        category_name,
        productname,
        photo=None,
        price=None,
        description="",
        
    ):
        sql = "INSERT INTO Products (category_name,productname, photo, price, description) VALUES($1, $2, $3, $4, $5) returning *"
        return await self.execute(
            sql,
            category_name,
            productname,
            photo,
            price,
            description,
            fetchrow=True,
        )
    
    async def get_categories(self):
        sql = "SELECT DISTINCT category_name FROM Products"
        return await self.execute(sql, fetch=True)

    async def count_products(self, category_name):
        sql = f"SELECT COUNT(*) FROM Products WHERE category_name='{category_name}'"
        return await self.execute(sql, fetchval=True)
    
    async def get_products(self, category_name):
        sql = f"SELECT * FROM Products WHERE category_name='{category_name}'"
        return await self.execute(sql, fetch=True)
    
    async def get_product_name(self, productname):
        sql = f"SELECT * FROM Products WHERE productname='{productname}'"
        return await self.execute(sql, fetchrow=True)   

    async def get_product(self, product_id):
        sql = f"SELECT * FROM Products WHERE id='{product_id}'"
        return await self.execute(sql, fetchrow=True)


    
    async def drop_products(self):
        await self.execute("DROP TABLE Products", execute=True)








    async def create_table_basket(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Baskeds (
        id SERIAL PRIMARY KEY,
        product_id INT NOT NULL,
        user_id BIGINT NOT NULL UNIQUE,
        count INT NOT NULL,
        productname VARCHAR(50)
        );
        """
        await self.execute(sql, execute=True)
   
    async def add_basket(self, user_id, product_id,count=1,productname=' '):
        sql = "INSERT INTO Baskeds (product_id,user_id,count,productname) VALUES($1, $2, $3,$4) returning *"
        return await self.execute(sql, user_id, product_id, count, productname, fetchrow=True)

    async def get_baskets(self, user_id):
        sql = f"SELECT * FROM Baskeds WHERE product_id={user_id}"
        return await self.execute(sql, fetch=True)
    async def all_bsk(self):
        sql = "SELECT * FROM Baskeds"
        return await self.execute(sql, fetch=True)
    
    async def get_count(self, user_id, product_id):
        sql = f"SELECT count FROM Baskeds WHERE user_id={product_id} AND product_id={user_id}"
        return await self.execute(sql, fetchval=True)



    async def update_count_pr(self, count, product_id):
        sql = "UPDATE Baskeds SET count=$1 WHERE user_id=$2"
        return await self.execute(sql, count, product_id, execute=True)
    
    async def update_pr_name(self, productname, product_id):
        sql = "UPDATE Baskeds SET productname=$1 WHERE user_id=$2"
        return await self.execute(sql, productname, product_id, execute=True)
    
    async def plus_count(self, user_id, product_id):
        sql = f"UPDATE Baskeds SET count=count + 1 WHERE user_id={user_id} AND product_id={product_id}"
        return await self.execute(sql, fetchval=True)

    async def minus_count(self, user_id, product_id):
        sql = f"UPDATE Baskeds SET count=count - 1 WHERE user_id={user_id} AND product_id={product_id}"
        return await self.execute(sql, fetchval=True)
    
    async def del_count(self, user_id, product_id):
        sql = f"DELETE FROM Baskeds WHERE user_id={user_id} AND product_id={product_id}"
        return await self.execute(sql, execute=True)
        
    async def drop_basket(self):
        await self.execute("DROP TABLE Baskeds", execute=True)
        
    async def delete_bsk(self,user_id):
        await self.execute(f"DELETE FROM Baskeds WHERE product_id={user_id}", execute=True)
