from __future__ import annotations
from dataclasses import dataclass
from mountain import Mountain

from typing import TYPE_CHECKING, Union
from data_structures.linked_stack import LinkedStack

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality


@dataclass
class TrailSplit:
    """
    A split in the trail.
       ___path_top____
      /               \
    -<                 >-path_follow-
      \__path_bottom__/
    """

    path_top: Trail
    path_bottom: Trail
    path_follow: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.path_follow.store


@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """Removes the mountain at the beginning of this series."""
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain in series before the current one."""
        return TrailSeries(mountain=mountain, following=Trail(store=self))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(
            path_top=Trail(store=None),
            path_bottom=Trail(store=None),
            path_follow=Trail(store=self)
        )

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        return TrailSeries(mountain=self.mountain,
                           following=Trail(store=TrailSeries(mountain=mountain, following=self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return TrailSeries(mountain=self.mountain, following=Trail(store=TrailSplit(
            path_top=Trail(store=None),
            path_bottom=Trail(store=None),
            path_follow=Trail(store=None)
        )))


TrailStore = Union[TrailSplit, TrailSeries, None]


@dataclass
class Trail:
    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """Adds a mountain before everything currently in the trail."""
        return Trail(store=TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """Adds an empty branch before everything currently in the trail."""
        return Trail(store=TrailSplit(path_top=Trail(None), path_bottom=Trail(None), path_follow=self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""

        current_trail = self.store
        path_stack = LinkedStack()

        while True:

            if isinstance(current_trail, TrailSplit):

                if current_trail.path_follow.store is not None:
                    path_stack.push(current_trail.path_follow.store)

                if personality.select_branch(current_trail.path_top, current_trail.path_bottom):
                    current_trail = current_trail.path_top.store
                else:
                    current_trail = current_trail.path_bottom.store

            if isinstance(current_trail, TrailSeries):
                if current_trail.mountain is not None:
                    personality.add_mountain(current_trail.mountain)

                current_trail = current_trail.following.store

            if current_trail is None:
                if not path_stack.is_empty():
                    current_trail = path_stack.pop()
                else:
                    break

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail.
        implement the method collect_all_mountains, which returns a list of Mountains that are within this trail.
        This should run in O(N) time, where N is the total number of mountains and branches combined.
        """
        mountain_list : list = []
        mystack = LinkedStack()
        mystack.push(self.store)

        while not mystack.is_empty():
            current_trail = mystack.pop()
            if isinstance(current_trail, TrailSplit):
                if current_trail.path_follow.store is not None:
                    mountain_list.append(current_trail.path_follow.store.mountain)
                mystack.push(current_trail.path_top.store)
                mystack.push(current_trail.path_bottom.store)
            if isinstance(current_trail, TrailSeries):
                if current_trail.mountain is not None:
                    mountain_list.append(current_trail.mountain)
                mystack.push(current_trail.following.store)
        return mountain_list

    def length_k_paths(self, k) -> list[list[Mountain]]:
        final_list: list[list[Mountain]] = []
        stack2 = LinkedStack()
        def inner_list(current_trail: Trail, trail_list: list) -> list[list[Mountain]]:
            if current_trail.store is None:
                while not stack2.is_empty():
                    trail_list.append(stack2.pop())
                return [trail_list[::-1]] if len(trail_list) == k else []
            else:
                paths = []
                if isinstance(current_trail.store, TrailSplit):
                    if current_trail.store.path_follow.store is not None:
                        trail_list.append(current_trail.store.path_follow.store.mountain)
                    tem_list_top = trail_list.copy()
                    paths.extend(inner_list(current_trail.store.path_top, tem_list_top))
                    tem_list_bottom = trail_list.copy()
                    paths.extend(inner_list(current_trail.store.path_bottom, tem_list_bottom))
                if isinstance(current_trail.store, TrailSeries):
                    if current_trail.store.mountain is not None:
                        stack2.push(current_trail.store.mountain)
                        paths.extend(inner_list(current_trail.store.following, trail_list))
                return paths
        final_list.extend(inner_list(self, []))
        return final_list
