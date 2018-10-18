# API For Melbourne House Market Prediction
## Authentication scheme for the consumers of your service
Using mLab to store users’ data.
**Login** 
Check the _USERS_ collections in database, find if there is a document match both username and password, then return successfully
**Signup** 
1. Check whether the new username is unique in the database, if it already exists, return `409 Username Taken`
2. Create new document to store username, password, email and name

## Get house data
- [x] Build data model
- [ ] Think about which database to use
- [ ] Take data from front-end to back-end
- [ ] Return data after processing to front-end