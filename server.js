console.log('May Node be with you')
const express = require('express')
const bodyParser= require('body-parser')
const app = express()

app.use(bodyParser.urlencoded({extended: true}))


// app.listen(3000, function() {
//   console.log('listening on 3000')
// })

app.get('/', (req, res) => {
	db.collection('quotes').find().toArray((err, result) => {
    if (err) return console.log(err)
    // renders index.ejs
    res.render('index.ejs', {quotes: result})
  })

})


const MongoClient = require('mongodb').MongoClient
var db

MongoClient.connect('mongodb://linayi0527:test1234@ds017553.mlab.com:17553/webcrawer', (err, database) => {
  // ... start the server

  if (err) return console.log(err)
  db = database
  app.listen(3000, () => {
    console.log('listening on 3000')
  })
})

app.post('/quotes', (req, res) => {
  db.collection('quotes').save(req.body, (err, result) => {
    if (err) return console.log(err)

    console.log('saved to database')
    res.redirect('/')
  })
  db.collection('quotes').find().toArray(function(err, results) {
  console.log(results)
  // send HTML file populated with quotes here
})
})
app.set('view engine', 'ejs')
