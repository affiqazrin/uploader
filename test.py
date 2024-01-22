if __name__ == '__main__':
    with app.app_context():
        app.secret_key = app.config['SECRET_KEY']

        # Check if the database is connected successfully
        try:
            db.create_all()
            print("Database connected successfully!")
        except Exception as e:
            app.logger.error(f"Error connecting to the database: {e}")

    app.run(debug=True,host='0.0.0.0', port=8888)
