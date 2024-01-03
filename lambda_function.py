import json

# function to do validation of slots data
def validate_data(slots):
    
   
    if slots['CostumerContactNumber'] is not None:
     
        if ( len(slots['CostumerContactNumber']['value']['originalValue'])<10 or len(slots['CostumerContactNumber']['value']['originalValue'])>10 ) :
        
          return { 
            'isValid': False,
            'invalidSlot': 'CostumerContactNumber',
            'message': 'Please enter proper contact number '
               }
       
      # valid slot
    return {'isValid': True}

# main event to handle lex request
def lambda_handler(event, context):
   
    # getting slots and intent information
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    
        
   
   # validating slot
    validation_result = validate_data(slots)
    
   # transfering the flow based on validation result       
    if event['invocationSource'] == 'DialogCodeHook':
          
      if not validation_result['isValid']:
            if 'message' in validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": validation_result['message']
                        }
                    ]
                }    
      else:
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name':intent,
                    'slots': slots
                    }
            }
        }        
     # fullfilment event after every slot is filled and valided    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        
        # getting user input slots value
        CostumerName=event['sessionState']['intent']['slots']['CostumerName']['value']['interpretedValue']
        RoomType=event['sessionState']['intent']['slots']['RoomType']['value']['interpretedValue']
       
        response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name':intent,
                'slots': slots,
                'state':'Fulfilled'
                
                      }
    
                   }
        ,
        "messages": [
            {
                "contentType": "PlainText",
                "content":"this is lambda success response"
            }
        ]
        
                  }
    # returning response back to lex      
    return response

