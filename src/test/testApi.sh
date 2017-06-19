echo "- Getting API info"
curl http://localhost:5000/
echo ""

echo "- Adding entry1 in bank1"
echo 'value1' | curl -X POST -d @- --header "Content-Type:text/plain" http://localhost:5000/bank/bank1/entry/entry1

echo ""
echo "- Getting entry1 of bank1"
curl http://localhost:5000/bank/bank1/entry/entry1

echo ""
echo "- Adding entry2 in bank1"
echo 'value2' | curl -X POST -d @- --header "Content-Type:text/plain" http://localhost:5000/bank/bank1/entry/entry2

echo ""
echo "- Getting entry2 of bank1"
curl http://localhost:5000/bank/bank1/entry/entry2


echo ""
echo "- Showing entries of bank1"
curl http://localhost:5000/bank/bank1/entries

echo ""
echo "- Showing entries of bank1"
curl -X PUT http://localhost:5000/bank/bank1?operation=reset

echo ""
echo "- Showing entries of bank1"
curl http://localhost:5000/bank/bank1/entries

echo ""
echo "- Showing banks"
curl http://localhost:5000/banks

echo ""