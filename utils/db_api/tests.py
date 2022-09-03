import asyncio

from db_commands import Database


async def test():
    db = Database()
    await db.create()

    print("Products jadvalini yaratamiz...")
    await db.drop_products()
    await db.create_table_products()
    await db.add_product(
        
        "🍒 Oziq-ovqat",
        "Ahmad Tea. Earl Grey",
        "https://ahmadtea.my/wp-content/uploads/2020/08/AHMA-BlackTeas-Earl-Grey-100tb-GT.png",
        10,
        "Ahmad choy",
    )
    await db.add_product(
        
        "🍒 Oziq-ovqat",
        "Ahmad Tea. English Brekafast",
        "https://dibaonline.de/media/image/product/196/lg/ahmad-tea-english-breakfast-500g-loose-leaf-tea.png",
        20,
         "Ahmad choy",
    )
    await db.add_product(
        
        "🍒 Oziq-ovqat",
       
        "Nescafe Gold",
        "https://www.nescafe.com/mt/sites/default/files/2020-07/nescafe-gold-blend-jar-front-pitch.png",
        15,
        "Discover our signature smooth, rich instant coffee. Coffee connoisseurs will appreciate the well-rounded taste and rich aroma in every cup. Our expertly crafted blend is great for all coffee drinking occasions, whenever you want to make a moment special. So why not relax, enjoy the now and savour the distinctive taste of this premium blend.",
    )
    await db.add_product(
        
        "🍒 Oziq-ovqat",
      
        "Nestle Sut. 1L",
        "https://100comments.com/wp-content/uploads/2017/03/nestle-just-milk-low-fat.jpg",
        2,
    )
    await db.add_product(
        "🖥️ Elektronika",
        "iPhone 13",
        "https://9to5mac.com/wp-content/uploads/sites/6/2021/09/iphone-13-pro-max-tidbits-9to5mac.jpg",
        1000,
        "Yangi iPhone 13",
    )
    await db.add_product(
        "🖥️ Elektronika",
        "macBook Air",
        "https://checheelectronics.co.ke/wp-content/uploads/2021/06/NL244a1b_2.jpg",
        1600,
         "Ahmad choy",
    )
    await db.add_product(
        "🖥️ Elektronika",
        "Ipad pro 5",
        "https://checheelectronics.co.ke/wp-content/uploads/2021/06/NL244a1b_2.jpg",
        1300,
         "6 / 256 gb",
    )
    
    await db.add_product(
        "🖥️ Elektronika",
        "Apple watch 3",
        "https://checheelectronics.co.ke/wp-content/uploads/2021/06/NL244a1b_2.jpg",
        100,
         "apple watch 3",
    )


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
