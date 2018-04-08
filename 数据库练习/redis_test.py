import redis


class Base(object):
    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)


class TestString(Base):

    def test_set(self):
        rest = self.r.set('user', "Jack")
        print(rest)
        return rest

    def test_get(self):
        rest = self.r.get('user')
        print(rest)
        return rest

    def test_mset(self):
        d = {
            'user1': 'Kim',
            'user2': 'Lola'
        }
        rest = self.r.mset(d)
        print(rest)
        return rest

    def test_mget(self):
        l = ['user', 'user1', 'user2']
        rest = self.r.mget(l)
        print(rest)
        return rest

    def test_del(self):
        rest = self.r.delete('user2')
        print(rest)
        return rest


class TestList(Base):

    def test_push(self):
        t = ('Bob', 'Lola')
        rest = self.r.lpush('l_eat', *t)
        print(rest)
        rest = self.r.lrange('l_eat', 0, -1)
        print(rest)

    def test_pop(self):
        rest = self.r.lpop('l_eat')
        print(rest)
        rest = self.r.lrange('l_eat', 0, -1)
        print(rest)


class TestSet(Base):

    def test_sadd(self):
        t = ('Bob', 'Lola')
        rest = self.r.sadd('s_eat', *t)
        print(rest)
        rest = self.r.smembers('s_eat')
        print(rest)

    def test_srem(self):
        t = ('Bob', 'Lola')
        rest = self.r.srem('s_eat', *t)
        print(rest)
        rest = self.r.smembers('s_eat')
        print(rest)

    def test_inter(self):
        rest = self.r.sinter('s_eat', 's_eat1')
        print(rest)

    def test_union(self):
        rest = self.r.sunion('s_eat', 's_eat1')
        print(rest)


def main():
    # obj = TestString()
    # obj.test_set()
    # obj.test_get()
    # obj.test_mset()
    # obj.test_mget()
    # obj.test_del()
    # obj = TestList()
    # obj.test_push()
    # obj.test_pop()
    obj = TestSet()
    # obj.test_sadd()
    # obj.test_srem()
    # obj.test_inter()
    obj.test_union()


if __name__ == '__main__':
    main()
