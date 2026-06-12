# Table data #
rm -rf data/
python main.py add-user --name "Alice" --email "alice@gmail.com"
python main.py add-user --name "Bob" --email "bob@gmail.com"
python main.py list-users
python main.py add-project --user "Alice" --title "CLI Tool" --description "Build CLI app" --due-date "2024-12-31"
python main.py list-projects --user "Alice"
python main.py add-task --project "CLI Tool" --title "Implement add-task" --assigned-to "Alice"
python main.py add-task --project "CLI Tool" --title "Setup database" --assigned-to "Bob"
python main.py list-tasks --project "CLI Tool"


# running tests #
pytest tests.py -v