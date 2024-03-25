from uuid import uuid4
from datetime import datetime
from typing import Any



class BaseModel:
    """Base class for all model classes with core functionalities."""

    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes new BaseModel instance.

        Args:
            kwargs (dict, optional): Keyword arguments for object creation.
                - created_at (str, optional): ISO formatted datetime string for creation time.
                - updated_at (str, optional): ISO formatted datetime string for update time.
                - Other custom attributes specific to the model.
        """
        self.id = str(uuid4())
        self.created_at = (
            datetime.now()
            if not kwargs.get("created_at")
            else datetime.strptime(kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
        )
        self.updated_at = self.created_at  # Update in `save`

        # Set other attributes from kwargs
        for key, value in kwargs.items():
            if key not in ("created_at", "updated_at"):
                setattr(self, key, value)

    def __str__(self) -> str:
        """
        Returns a string representation of the BaseModel object.

        Returns:
            str: A formatted string with class name, ID, and attributes.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self) -> None:
        """
        Updates the updated_at timestamp for the object.

        Triggers storage update (implementation depends on the storage module).
        """
        self.updated_at = datetime.now()
        storage.save(self)  # Assuming storage is imported and has a save method

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the BaseModel object.

        Returns:
            dict: A dictionary containing all attributes and ISO formatted timestamps.
        """
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = my_dict["created_at"].isoformat()
        my_dict["updated_at"] = my_dict["updated_at"].isoformat()
        return my_dict
