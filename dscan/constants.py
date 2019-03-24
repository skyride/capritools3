from django.db.models import Q

from sde.models import Type


super_groups = [30, 659]
cap_groups = [883, 547, 485, 1538, 513, 902]

logistics_cruisers = [625, 634, 620, 49712, 631]
logistics_frigates = [582, 599, 590, 592]
logistics_groups = [832, 1527]
logistics = Type.objects.filter(
    Q(id__in=logistics_cruisers + logistics_frigates) |
    Q(group_id__in=logistics_groups)
)

support_groups = [906, 1534, 893, 1972, 833, 894, 541]
support_types = [628, 630, 632, 633, 2161, 584, 590, 609]
support = Type.objects.filter(
    Q(id__in=support_types) |
    Q(group_id__in=support_groups)
)