class DbRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "product":
            return "products"
        return

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "product":
            return "products"
        return

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == "product" or obj2._meta.app_label == "product":
            return True
        return

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == "product":
            return db == "products"
        return
