import F_vertify
import random

a = F_vertify.hand_vertify(F_vertify.vertify_thumb(random.uniform(0,40)),
                       F_vertify.vertify_index(random.uniform(0,40)),
                       F_vertify.vertify_middle(random.uniform(0,40)),
                       F_vertify.vertify_ring(random.uniform(0,40)),
                       F_vertify.vertify_pinky(random.uniform(0,40))
)
print(a)