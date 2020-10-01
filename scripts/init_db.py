# This script is to get some data on the database incase the database needs to be deleted

import os

os.environ['DJANGO_SETTINGS_MODULE']='bookstore.settings'

from store.models import Genre, Book, Author, Publisher

GENRES = [
    'Action',
    'Adventure',
    'Art/architecture',
    'Alternate history',
    'Autobiography',
    'Anthology',
    'Biography',
    'Chick lit',
    'Business',
    'Economics',
    'Finance',
    'Children\'s',
    'Crafts/hobbies',
    'Classic',
    'Cookbook',
    'Comic book',
    'Diary',
    'Coming-of-age',
    'Dictionary',
    'Crime',
    'Encyclopedia',
    'Drama',
    'Guide',
    'Fairytale',
    'Health/fitness',
    'Fantasy',
    'History',
    'Graphic novel',
    'Home and Garden',
    'Historical fiction',
    'Humor',
    'Horror',
    'Journal',
    'Mystery',
    'Math',
    'Paranormal romance',
    'Memoir',
    'Picture book',
    'Philosophy',
    'Poetry',
    'Prayer',
    'Political thriller',
    'Religion, spirituality, and new age',
    'Religion',
    'Romance',
    'Textbook',
    'Satire',
    'True crime',
    'Science fiction',
    'Review',
    'Short story',
    'Science',
    'Suspense',
    'Self help',
    'Thriller',
    'Sports and leisure',
    'Western',
    'Travel',
    'Young adult',
    'Other',
    'Computer Science',
    'Fiction',
    'Nonfiction',
    'War',
]

AUTHORS = [
    {'first_name': 'W.', 'middle_name': '', 'last_name': 'Stevens'},
    {'first_name': 'Stephen', 'middle_name': '', 'last_name': 'Rago'},
    {'first_name': 'Gregory', 'middle_name': '', 'last_name': 'Zuckerman'},
    {'first_name': 'John', 'middle_name': '', 'last_name': 'Carreyrou'},
    {'first_name': 'Jon', 'middle_name': '', 'last_name': 'Krakauer'},
    {'first_name': 'Amor', 'middle_name': '', 'last_name': 'Towles'},
    {'first_name': 'Tara', 'middle_name': '', 'last_name': 'Westover'},
    {'first_name': 'Mark', 'middle_name': '', 'last_name': 'Sullivan'},
    {'first_name': 'Anthony', 'middle_name': '', 'last_name': 'Doerr'},
    {'first_name': 'GB', 'middle_name': '', 'last_name': 'Tran'},
    {'first_name': 'Joseph', 'middle_name': '', 'last_name': 'Fink'},
    #{'first_name': '', 'middle_name': '', 'last_name': ''},
]

PUBLISHERS = {
    'Addison-Wesley Professional',
    'Portfolio',
    'Vintage',
    'Anchor Books',
    'Penguin Books',
    'Random House',
    'Lake Union Publishing',
    'Scribner',
    'Villard',
    'Harper Perennial',
}

# You are gonna need to go and upload the images to the admin page.
BOOKS = [
    {'title': 'Advanced Programming in the UNIX Environment', 'summary': 'For more than twenty years, serious C programmers have relied on one book for practical, in-depth knowledge of the programming interfaces that drive the UNIX and Linux kernels: W. Richard Stevens’ Advanced Programming in the UNIX® Environment. Now, once again, Rich’s colleague Steve Rago has thoroughly updated this classic work. The new third edition supports today’s leading platforms, reflects new technical advances and best practices, and aligns with Version 4 of the Single UNIX Specification.', 'authors': ['Stevens', 'Rago'], 'genres': ['TextBook','Computer Science'], 'publication_year': 2013, 'isbn': '9780321637734', 'rating': 4.5, 'edition': 3, 'publisher': 'Addison-Wesley Professional', 'selling_price': 60.98, 'buying_price': 42.83, 'stock': 6},
    {'title': 'The Man Who Solved the Market: How Jim Simons Launched the Quant Revolution', 'summary': "Jim Simons is the greatest money maker in modern financial history. No other investor--Warren Buffett, Peter Lynch, Ray Dalio, Steve Cohen, or George Soros--can touch his record. Since 1988, Renaissance's signature Medallion fund has generated average annual returns of 66 percent. The firm has earned profits of more than $100 billion; Simons is worth twenty-three billion dollars.\n\nDrawing on unprecedented access to Simons and dozens of current and former employees, Zuckerman, a veteran Wall Street Journal investigative reporter, tells the gripping story of how a world-class mathematician and former code breaker mastered the market. Simons pioneered a data-driven, algorithmic approach that's sweeping the world.\n\nAs Renaissance became a market force, its executives began influencing the world beyond finance. Simons became a major figure in scientific research, education, and liberal politics. Senior executive Robert Mercer is more responsible than anyone else for the Trump presidency, placing Steve Bannon in the campaign and funding Trump's victorious 2016 effort. Mercer also impacted the campaign behind Brexit.\n\nThe Man Who Solved the Market is a portrait of a modern-day Midas who remade markets in his own image, but failed to anticipate how his success would impact his firm and his country. It's also a story of what Simons's revolution means for the rest of us.", 'authors': ['Zuckerman'], 'genres': ['Finance', 'Biography', 'Economics'], 'publication_year': 2019, 'isbn': '073521798X', 'rating': 4.7, 'edition': 0, 'publisher': 'Portfolio', 'selling_price': 24.99, 'buying_price': 18.77, 'stock': 3},
    {'title': 'Bad Blood: Secrets and Lies in a Silicon Valley Startup', 'summary': "In 2014, Theranos founder and CEO Elizabeth Holmes was widely seen as the next Steve Jobs: a brilliant Stanford dropout whose startup “unicorn” promised to revolutionize the medical industry with its breakthrough device, which performed the whole range of laboratory tests from a single drop of blood. Backed by investors such as Larry Ellison and Tim Draper, Theranos sold shares in a fundraising round that valued the company at more than $9 billion, putting Holmes’s worth at an estimated $4.5 billion. There was just one problem: The technology didn’t work. Erroneous results put patients in danger, leading to misdiagnoses and unnecessary treatments. All the while, Holmes and her partner, Sunny Balwani, worked to silence anyone who voiced misgivings—from journalists to their own employees.\n\nRigorously reported and fearlessly written, Bad Blood is a gripping story of the biggest corporate fraud since Enron—a tale of ambition and hubris set amid the bold promises of Silicon Valley.", 'authors': ['Carreyrou'], 'genres': ['Business', 'True crime'], 'publication_year': 2018, 'isbn': '0525431993', 'rating': 5, 'edition': 0, 'publisher': 'Vintage', 'selling_price': 19.99, 'buying_price': 12.49, 'stock': 4},
    {'title': 'Into the Wild', 'summary': 'In April 1992 a young man from a well-to-do family hitchhiked to Alaska and walked alone into the wilderness north of Mt. McKinley. He had given $25,000 in savings to charity, abandoned his car and most of his possessions, burned all the cash in his wallet, and invented a new life for himself. Four months later, his decomposed body was found by a moose hunter.  How Christopher Johnson McCandless came to die is the unforgettable story of Into the Wild.', 'authors': ['Krakauer'], 'genres': ['Adventure', 'Travel'], 'publication_year': 1997, 'isbn': '0385486804', 'rating': 4.2, 'edition': 0, 'publisher': 'Anchor Books', 'selling_price': 9.99, 'buying_price': 6.49, 'stock': 13},
    {'title': 'A Gentleman in Moscow', 'summary': "In 1922, Count Alexander Rostov is deemed an unrepentant aristocrat by a Bolshevik tribunal, and is sentenced to house arrest in the Metropol, a grand hotel across the street from the Kremlin. Rostov, an indomitable man of erudition and wit, has never worked a day in his life, and must now live in an attic room while some of the most tumultuous decades in Russian history are unfolding outside the hotel’s doors. Unexpectedly, his reduced circumstances provide him entry into a much larger world of emotional discovery.\n\nBrimming with humor, a glittering cast of characters, and one beautifully rendered scene after another, this singular novel casts a spell as it relates the count’s endeavor to gain a deeper understanding of what it means to be a man of purpose.", 'authors': ['Towles'], 'genres': ['Thriller', 'Political thriller', 'History'], 'publication_year': 2019, 'isbn': '0143110438', 'rating': 4.3, 'edition': 0, 'publisher': 'Penguin Books', 'selling_price': 12.99, 'buying_price': 8.49, 'stock': 4},
    {'title': 'Educated: A Memoir', 'summary': "Born to survivalists in the mountains of Idaho, Tara Westover was seventeen the first time she set foot in a classroom. Her family was so isolated from mainstream society that there was no one to ensure the children received an education, and no one to intervene when one of Tara’s older brothers became violent. When another brother got himself into college, Tara decided to try a new kind of life. Her quest for knowledge transformed her, taking her over oceans and across continents, to Harvard and to Cambridge University. Only then would she wonder if she’d traveled too far, if there was still a way home.", 'authors': ['Westover'], 'genres': ['Biography', 'Religion'], 'publication_year': 2018, 'isbn': '978-0399590504', 'rating': 4.3, 'edition': 0, 'publisher': 'Random House', 'selling_price': 15.99, 'buying_price': 11.99, 'stock': 13},
    {'title': 'Beneath a Scarlet Sky', 'summary': "Pino Lella wants nothing to do with the war or the Nazis. He’s a normal Italian teenager—obsessed with music, food, and girls—but his days of innocence are numbered. When his family home in Milan is destroyed by Allied bombs, Pino joins an underground railroad helping Jews escape over the Alps, and falls for Anna, a beautiful widow six years his senior.\n\nIn an attempt to protect him, Pino’s parents force him to enlist as a German soldier—a move they think will keep him out of combat. But after Pino is injured, he is recruited at the tender age of eighteen to become the personal driver for Adolf Hitler’s left hand in Italy, General Hans Leyers, one of the Third Reich’s most mysterious and powerful commanders.\n\nNow, with the opportunity to spy for the Allies inside the German High Command, Pino endures the horrors of the war and the Nazi occupation by fighting in secret, his courage bolstered by his love for Anna and for the life he dreams they will one day share.", 'authors': ['Sullivan'], 'genres': ['Biography', 'History'], 'publication_year': 2017, 'isbn': '1503943372', 'rating': 4.1, 'edition': 0, 'publisher': 'Lake Union Publishing', 'selling_price': 11.99, 'buying_price': 7.59, 'stock': 4},
    {'title': 'All the Light We Cannot See', 'summary': "From the highly acclaimed, multiple award-winning Anthony Doerr, the stunningly beautiful instant New York Times bestseller about a blind French girl and a German boy whose paths collide in occupied France as both try to survive the devastation of World War II.\n\nMarie-Laure lives in Paris near the Museum of Natural History, where her father works. When she is twelve, the Nazis occupy Paris and father and daughter flee to the walled citadel of Saint-Malo, where Marie-Laure’s reclusive great uncle lives in a tall house by the sea. With them they carry what might be the museum’s most valuable and dangerous jewel.\n\nIn a mining town in Germany, Werner Pfennig, an orphan, grows up with his younger sister, enchanted by a crude radio they find that brings them news and stories from places they have never seen or imagined. Werner becomes an expert at building and fixing these crucial new instruments and is enlisted to use his talent to track down the resistance. Deftly interweaving the lives of Marie-Laure and Werner, Doerr illuminates the ways, against all odds, people try to be good to one another.\n\nDoerr’s “stunning sense of physical detail and gorgeous metaphors” (San Francisco Chronicle) are dazzling. Ten years in the writing, a National Book Award finalist, All the Light We Cannot See is a magnificent, deeply moving novel from a writer “whose sentences never fail to thrill” (Los Angeles Times).", 'authors': ['Doerr'], 'genres': ['History', 'War', 'Fiction'], 'publication_year': 2017, 'isbn': '1501173219', 'rating': 4.3, 'edition': 0, 'publisher': 'Scribner', 'selling_price': 10.15, 'buying_price': 8.85, 'stock': 9},
    {'title': 'Vietnamerica: A Family\'s Journey', 'summary': "GB Tran is a young Vietnamese American artist who grew up distant from (and largely indifferent to) his family's history. Born and raised in South Carolina as a son of immigrants, he knew that his parents had fled Vietnam during the fall of Saigon. But even as they struggled to adapt to life in America, they preferred to forget the past--and to focus on their children's future. It was only in his late twenties that GB began to learn their extraordinary story. When his last surviving grandparents die within months of each other, GB visits Vietnam for the first time and begins to learn the tragic history of his family, and of the homeland they left behind.\n\nIn this family saga played out in the shadow of history, GB uncovers the root of his father's remoteness and why his mother had remained in an often fractious marriage; why his grandfather had abandoned his own family to fight for the Viet Cong; why his grandmother had had an affair with a French soldier. GB learns that his parents had taken harrowing flight from Saigon during the final hours of the war not because they thought America was better but because they were afraid of what would happen if they stayed. They entered America--a foreign land they couldn't even imagine--where family connections dissolved and shared history was lost within a span of a single generation.\n\nIn telling his family's story, GB finds his own place in this saga of hardship and heroism. Vietnamerica is a visually stunning portrait of survival, escape, and reinvention--and of the gift of the American immigrants' dream, passed on to their children. Vietnamerica is an unforgettable story of family revelation and reconnection--and a new graphic-memoir classic.", 'authors': ['Tran'], 'genres': ['History', 'Comic book','Memoir'], 'publication_year': 2011, 'isbn': '0345508726', 'rating': 3.9, 'edition': 0, 'publisher': 'Villard', 'selling_price': 16.99, 'buying_price': 12.59, 'stock': 3},
    {'title': 'Welcome to Night Vale', 'summary': "From the creators of the #1 international hit podcast Welcome to Night Vale comes an imaginative mystery of appearances and disappearances that is also a poignant look at the ways in which we all struggle to find ourselves . . . no matter where we live.\n\nWelcome to Night Vale . . . a friendly desert community somewhere in the American Southwest. In this ordinary little town where ghosts, angels, aliens, and government conspiracies are commonplace parts of everyday life, the lives of two women, with two mysteries, are about to converge.\n\nPawnshop proprietor Jackie Fierro abides by routine. But a crack appears in the standard order of her perpetually nineteen-year-old life when a mysterious man in a tan jacket gives her a slip of paper marked by two pencil-smudged words: KING CITY. Everything about the man unsettles her, especially the paper that she cannot remove from her hand. Yet when Jackie puts her life on hold to search for the man, no one who meets him can seem to remember anything about him.\n\nDiane Crayton’s fifteen-year-old son, Josh, is moody and a shape-shifter. Lately, Diane has started to see the boy’s father everywhere she goes, looking the same as he did the day he left when they were teenagers. Josh is growing ever more curious about his estranged father—leading to a disaster Diane can see coming but is helpless to prevent.\n\nDiane’s search to reconnect with her son and Jackie’s search to reclaim her routine life draw them increasingly closer to each other, and to this place that may hold the key to their mysteries and their futures . . . if they can ever find it.", 'authors': ['Fink'], 'genres': ['Fiction', 'Horror', 'Fantasy'], 'publication_year': 2017, 'isbn': '978-0062351432', 'rating': 4.4, 'edition': 0, 'publisher': 'Harper Perennial', 'selling_price': 12.99, 'buying_price': 8.38, 'stock': 6},
    #{'title': '', 'summary': "", 'authors': [], 'genres': [], 'publication_year': 0, 'isbn': '', 'rating': 0, 'edition': 0, 'publisher': 'Anchor Books', 'selling_price': 0, 'buying_price': 0, 'stock': 0},
]

for genre in GENRES:
    Genre.objects.create(genre=genre)

for author in AUTHORS:
    Author.objects.create(first_name=author['first_name'], last_name=author['last_name'])

for publisher in PUBLISHERS:
    Publisher.objects.create(name=publisher)

i = 0
for book in BOOKS:
    i += 1
    publisher = Publisher.objects.filter(name=book['publisher']).first()
    b = Book.objects.create(title=book['title'],
                            summary=book['summary'],
                            publication_year=book['publication_year'],
                            isbn=book['isbn'],
                            selling_price=book['selling_price'],
                            buying_price=book['buying_price'],
                            rating=book['rating'],
                            edition=book['edition'],
                            publisher=publisher,
                            featured=(i%3==0),
                          )
    for author in book['authors']:
        b.authors.add(Author.objects.filter(last_name=author).first())
    for genre in book['genres']:
        b.genres.add(Genre.objects.filter(genre=genre).first())
