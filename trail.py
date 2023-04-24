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
        return TrailSeries(mountain=mountain,following=Trail(store=self))

    def add_empty_branch_before(self) -> TrailStore:
        """Adds an empty branch, where the current trailstore is now the following path."""
        return TrailSplit(
            path_top=Trail(store=None),
            path_bottom=Trail(store=None),
            path_follow=Trail(store=self)
        )

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """Adds a mountain after the current mountain, but before the following trail."""
        return TrailSeries(mountain=self.mountain,following=Trail(store=TrailSeries(mountain=mountain,following=self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """Adds an empty branch after the current mountain, but before the following trail."""
        return TrailSeries(mountain=self.mountain,following=Trail(store=TrailSplit(
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
        stack1 = LinkedStack()
        stack2 = LinkedStack()
        trail = self.store
        while trail is not None:
            if isinstance(trail, TrailSplit):
                if trail.path_follow.store is not None:
                    stack1.push(trail.path_follow.store.mountain)
                if personality.select_branch(trail.path_top, trail.path_bottom):
                    trail = trail.path_top.store
                else:
                    trail = trail.path_bottom.store
            elif isinstance(trail, TrailSeries):
                if trail.mountain is not None:
                    print('mountain:', trail.mountain)
                    stack2.push(trail.mountain)
                trail = trail.following.store
        for _ in range(len(stack2)):
            stack1.push(stack2.pop())
        for _ in range(len(stack1)):
            item = stack1.pop()
            personality.add_mountain(item)
        print(personality.mountains)

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def length_k_paths(self, k) -> list[list[Mountain]]:  # Input to this should not exceed k > 50, at most 5 branches.
        """
        Returns a list of all paths of containing exactly k mountains.
        Paths are represented as lists of mountains.

        Paths are unique if they take a different branch, even if this results in the same set of mountains.
        """
        raise NotImplementedError()
