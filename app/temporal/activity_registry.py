from app.temporal.activities import (
    verify_user_activity,
    check_inventory_activity,
    create_order_activity,
)

ACTIVITY_REGISTRY = {
    "verify_user": verify_user_activity,
    "check_inventory": check_inventory_activity,
    "create_order": create_order_activity,
}
