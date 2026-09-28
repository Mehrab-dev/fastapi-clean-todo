
from app.domain.entities.user_entity import User as user_entity
from app.domain.entities.profile_entity import Profile as profile_entity
from app.domain.entities.task_entity import Task as task_entity
from app.infrastructure.database import models



class UserMapper:
    @staticmethod
    def to_domain(model: models.UserModel) -> user_entity:
        return user_entity(
            id=model.id,
            email=model.email,
            password=model.password,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: user_entity) -> models.UserModel:
        return models.UserModel(
            id=entity.id,
            email=entity.email,
            password=entity.password,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )



class ProfileMapper:
    @staticmethod
    def to_domain(model: models.ProfileModel) -> profile_entity:
        return profile_entity(
            id=model.id,
            user_id=model.user_id,
            first_name=model.first_name,
            last_name=model.last_name,
            bio=model.bio,
            image=model.image,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: profile_entity) -> models.ProfileModel:
        return models.ProfileModel(
            id=entity.id,
            user_id=entity.user_id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            bio=entity.bio,
            image=entity.image,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )



class TaskMapper:
    @staticmethod
    def to_domain(model: models.TaskModel) -> task_entity:
        return task_entity(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            description=model.description,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def to_model(entity: task_entity) -> models.TaskModel:
        return models.TaskModel(
            id=entity.id,
            user_id=entity.user_id,
            title=entity.title,
            description=entity.description,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )