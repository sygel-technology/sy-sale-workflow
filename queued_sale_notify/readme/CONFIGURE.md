To configure this module, you need to:

1. Go to Sales / Configuration / Sale Order Types.
2. On a sale order type form view, go to the notifications notebook and create a notification for that type. Have 3 sheets and models to choose, mail notifications, note notifications and activity notifications.
3. Fill the delay time, trigger state, and notification data.
4. The records that have a configured notification on its type, will queue a notification with the setted delay when the record reaches the setted trigger state.
 
This module only has one trigger state, confirmed sale orders. To add a new one you have to create a new module that depends on this one.
