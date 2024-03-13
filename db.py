import sqlalchemy as sa
from sqlalchemy.orm import Mapped, Session, DeclarativeBase, mapped_column
db_password = ""
engine = sa.create_engine('postgresql://postgres:' + db_password + '@localhost:5432/test', echo=True)
conn = engine.connect()
session = Session(engine)
metadata = sa.MetaData()
storage = {
    'baseline': 'baseline_matrix_1',
    'discounts': {
        '168': 'discount_matrix_3',
        '290': 'discount_matrix_2'
    }
}
databases = {}


def getPriceWithData(mIDs, lIDs, user_segments_ID):
    listmatrix = []
    discount_storage = storage['discounts']
    for segment in user_segments_ID:
        segment_matrix = discount_storage.get(str(segment))
        if segment_matrix:
            if segment_matrix not in listmatrix:
                listmatrix.append(segment_matrix)
    for matrix in listmatrix:
        discount_table = databases.get(matrix)
        if discount_table == None:
            discount_table = sa.Table(matrix, metadata,
                                      sa.Column('microcategory_id', sa.Integer, primary_key=True),
                                      sa.Column('location_id', sa.Integer),
                                      sa.Column('price', sa.Integer))
            databases[matrix] = discount_table
        for lID in lIDs:
            for mID in mIDs:
                query = (sa.select(discount_table.c.price)
                         .filter(sa.and_(discount_table.c.microcategory_id == mID, discount_table.c.location_id == lID))
                         .select_from(discount_table))
                res = session.execute(query)
                result = res.all()
                if len(result) != 0:
                    for key in discount_storage:
                        if matrix == discount_storage.get(key):
                            return {"price": result[0][0], "microcategory_id": mID, "location_id": lID, 'user_segment_id': key}
    baseline_table = databases.get(storage['baseline'])
    if baseline_table == None:
        baseline_table = sa.Table(storage['baseline'], metadata,
                                  sa.Column('microcategory_id', sa.Integer, primary_key=True),
                                  sa.Column('location_id', sa.Integer),
                                  sa.Column('price', sa.Integer))
        databases[storage['baseline']] = baseline_table
    query = sa.select(baseline_table.c.price).filter(
        sa.and_(baseline_table.c.microcategory_id == mIDs[0], baseline_table.c.location_id == lIDs[0])).select_from(
        baseline_table)
    res = session.execute(query)
    result = res.all()
    price = result[0][0]
    return {"price": price, "microcategory_id": mIDs[0], "location_id": lIDs[0], 'user_segment_id': 0}


#def createPriceWithData(mID, lID):
