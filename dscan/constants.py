from django.db.models import Q

from sde.models import Type


SUPER_GROUPS = [30, 659]
CAP_GROUPS = [883, 547, 485, 1538, 513, 902]

LOGISTICS_CRUISERS = [625, 634, 620, 49712, 631]
LOGISTICS_FRIGATES = [582, 599, 590, 592]
LOGISTICS_GROUPS = [832, 1527]
LOGISTICS = Type.objects.filter(
    Q(id__in=LOGISTICS_CRUISERS + LOGISTICS_FRIGATES) |
    Q(group_id__in=LOGISTICS_GROUPS)
)

SUPPORT_GROUPS = [906, 1534, 893, 1972, 833, 894, 541]
SUPPORT_TYPES = [628, 630, 632, 633, 2161, 584, 590, 609]
SUPPORT = Type.objects.filter(
    Q(id__in=SUPPORT_TYPES) |
    Q(group_id__in=SUPPORT_GROUPS)
)