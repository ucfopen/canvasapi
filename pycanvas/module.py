from canvas_object import CanvasObject
from exceptions import RequiredFieldMissing
from paginated_list import PaginatedList
from util import combine_kwargs


class Module(CanvasObject):

    def __str__(self):
        return "id: %s, name: %s" % (
            self.id,
            self.name,
        )

    def edit(self, **kwargs):
        """
        Update and return an existing module

        :calls: `PUT /api/v1/courses/:course_id/modules/:id`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.update>
        :rtype: :class:`Module`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s' % (self.course_id, self.id),
            **kwargs
        )
        module_json = response.json()
        module_json.update({'course_id': self.course_id})

        return Module(self._requester, module_json)

    def delete(self):
        """
        Delete a module

        :calls: `DELETE /api/v1/courses/:course_id/modules/:id`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.destroy>
        :rtype: :class:`Module`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/modules/%s' % (self.course_id, self.id),
        )
        module_json = response.json()
        module_json.update({'course_id': self.course_id})

        return Module(self._requester, module_json)

    def relock(self):
        """
        Resets module progressions to their default locked state and recalculates
        them based on the current requirements.

        Adding progression requirements to an active course will notlock students
        out of modules they have already unlocked unless this action is called.

        :calls: `PUT /api/v1/courses/:course_id/modules/:id/relock`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.relock>
        :rtype: :class:`Module`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s/relock' % (self.course_id, self.id),
        )
        module_json = response.json()
        module_json.update({'course_id': self.course_id})

        return Module(self._requester, module_json)

    def list_module_items(self):
        """
        List the items in a module

        :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.index>
        :rtype: :class:`PaginatedList` of :class:`ModuleItem`
        """
        return PaginatedList(
            ModuleItem,
            self._requester,
            'GET',
            'courses/%s/modules/%s/items' % (self.course_id, self.id),
            {'course_id': self.course_id}
        )

    def get_module_item(self, module_item_id):
        """
        Get information about a single module item

        :calls: `GET /api/v1/courses/:course_id/modules/:module_id/items/:id`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.show>
        :rtype: :class:`ModuleItem`
        """
        response = self._requester.request(
            'GET',
            'courses/%s/modules/%s/items/%s' % (self.course_id, self.id, module_item_id),
        )
        module_item_json = response.json()
        module_item_json.update({'course_id': self.course_id})

        return ModuleItem(self._requester, module_item_json)

    def create_module_item(self, module_item, **kwargs):
        """
        Create and return a new module item

        :calls: `POST /api/v1/courses/:course_id/modules/:module_id/items`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.create>
        :param type: str
        :param content_id: str
        :rtype: :class:`ModuleItem`
        """
        if isinstance(module_item, dict) and 'type' in module_item:
            if 'content_id' in module_item:
                kwargs['module_item'] = module_item
            else:
                raise RequiredFieldMissing("Dictionary with key 'content_id' is required.")
        else:
            raise RequiredFieldMissing("Dictionary with key 'type' is required.")

        response = self._requester.request(
            'POST',
            'courses/%s/modules/%s/items' % (self.course_id, self.id),
            **combine_kwargs(**kwargs)
        )
        module_item_json = response.json()
        module_item_json.update({'course_id': self.course_id})

        return ModuleItem(self._requester, module_item_json)


class ModuleItem(CanvasObject):

    def __str__(self):
        return "id: %s, title: %s, description: %s" % (
            self.id,
            self.title,
            self.module_id
        )

    def edit(self, **kwargs):
        """
        Update and return an existing module

        :calls: `PUT /api/v1/courses/:course_id/modules/:id`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.update>
        :rtype: :class:`Module`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s/items/%s' % (self.course_id, self.module_id, self.id),
            **kwargs
        )
        module_item_json = response.json()
        module_item_json.update({'course_id': self.course_id})

        return ModuleItem(self._requester, module_item_json)

    def delete(self):
        """
        Delete a module item

        :calls: `DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id`
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.destroy>
        :rtype: :class:`ModuleItem`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/modules/%s/items/%s' % (self.course_id, self.module_id, self.id),
        )
        module_item_json = response.json()
        module_item_json.update({'course_id': self.course_id})

        return ModuleItem(self._requester, module_item_json)

    def complete(self):
        """
        Mark a module item as done
        :calls: `PUT /api/v1/courses/:course_id/modules/:module_id/items/:id/done`,
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done>
        :rtype: :class:`ModuleItem`
        """
        response = self._requester.request(
            'PUT',
            'courses/%s/modules/%s/items/%s/done' % (self.course_id, self.module_id, self.id),
        )
        module_item_json = response.json()
        module_item_json.update({'course_id': self.course_id})

        return ModuleItem(self._requester, module_item_json)

    def uncomplete(self):
        """
        Mark a module item as not done
        :calls: `DELETE /api/v1/courses/:course_id/modules/:module_id/items/:id/done`,
        <https://canvas.instructure.com/doc/api/modules.html#method.context_module_items_api.mark_as_done>
        :rtype: :class:`ModuleItem`
        """
        response = self._requester.request(
            'DELETE',
            'courses/%s/modules/%s/items/%s/done' % (self.course_id, self.module_id, self.id),
        )
        module_item_json = response.json()
        module_item_json.update({'course_id': self.course_id})

        return ModuleItem(self._requester, module_item_json)
