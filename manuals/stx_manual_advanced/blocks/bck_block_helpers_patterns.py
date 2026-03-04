"""Block helpers: 3 usage patterns explained and demonstrated.

This block explains the hybrid block helpers system available in StreamTeX.
Shows all 3 patterns with live code examples.
"""

from streamtex import st_write, st_space, st_list
from custom.styles import Styles as s
from blocks.helpers import (
    show_code, show_explanation, show_details,
    demonstrate_simple_pattern,
    demonstrate_config_pattern,
    demonstrate_oop_pattern,
    demonstrate_expert_pattern,
)


class BlockStyles:
    """Local styles for this block."""
    pass


def build():
    """Build the block helpers patterns demonstration block."""

    # ========================================================================
    # INTRODUCTION
    # ========================================================================
    st_write(s.project.titles.page_title, "Block Helpers: 3 Usage Patterns")
    st_space("v", 1)
    st_write(s.large, """
StreamTeX provides a hybrid block helpers system with 3 usage patterns.
Choose the one that fits your needs, from simple to advanced.
    """)

    # ========================================================================
    # PATTERN 1: CONFIG INJECTION (DI)
    # ========================================================================
    st_write(s.project.titles.section_title, "Pattern 1: Config Injection (Recommended)")
    st_space("v", 1)

    show_explanation("""
The recommended pattern for most projects.

Define your project's styles once in ProjectBlockHelperConfig.

All helpers automatically use your styles globally.
    """)

    st_write(s.project.titles.feature_title, "How it works:")
    with st_list(s.large, s.large, list_type="ol") as l:
        with l.item():
            st_write(s.large, "Define ", (s.bold, "ProjectBlockHelperConfig"), " with your styles")
        with l.item():
            st_write(s.large, "Call ", (s.bold, "set_block_helper_config()"), " once at startup")
        with l.item():
            st_write(s.large, "All ", (s.bold, "show_code()"), ", ", (s.bold, "show_explanation()"), ", etc. use your styles automatically")

    st_write(s.project.titles.feature_title, "Code example:")
    show_code("""
from streamtex import BlockHelperConfig, set_block_helper_config
from custom.styles import Styles as s

class ProjectBlockHelperConfig(BlockHelperConfig):
    def get_code_style(self):
        return s.project.containers.code_box

    def get_explanation_style(self):
        return s.project.containers.explanation_box

set_block_helper_config(ProjectBlockHelperConfig())

# Now all helpers use your styles!
from blocks.helpers import show_code
show_code("print('hello')")  # Uses s.project.containers.code_box
    """, language="python")

    st_write(s.project.titles.feature_title, "Benefits:")
    with st_list(s.large, s.large, list_type="ul") as l:
        with l.item():
            st_write(s.large, (s.bold, "DRY"), ": Define styles once, use everywhere")
        with l.item():
            st_write(s.large, (s.bold, "Simple"), ": No parameters needed")
        with l.item():
            st_write(s.large, (s.bold, "Global"), ": Consistent styling across all blocks")
        with l.item():
            st_write(s.large, (s.bold, "Flexible"), ": Can still override per-call with style= parameter")

    st_space("v", 2)

    # ========================================================================
    # PATTERN 2: STANDALONE FUNCTIONS (Simple)
    # ========================================================================
    st_write(s.project.titles.section_title, "Pattern 2: Standalone Functions (Simple)")
    st_space("v", 1)

    show_explanation("""
Simple pattern: import and use functions directly.

Works great with Config Injection (Pattern 1).

Can override style per-call if needed.
    """)

    st_write(s.project.titles.feature_title, "How it works:")
    with st_list(s.large, s.large, list_type="ol") as l:
        with l.item():
            st_write(s.large, "Import helpers from ", (s.bold, "streamtex"), " or local blocks")
        with l.item():
            st_write(s.large, "Call them directly with optional ", (s.bold, "style="), " override")
        with l.item():
            st_write(s.large, "Styles from config are used automatically")

    st_write(s.project.titles.feature_title, "Code example:")
    show_code("""
from blocks.helpers import show_code, show_explanation
from custom.styles import Styles as s

# Uses config-injected style
show_code("print('hello')")

# Override with custom style
show_code("print('world')", style=s.custom.special_box)

# Standalone explanation
show_explanation('''
This shows how to use the simple pattern.
Just call the function!
''')
    """, language="python")

    st_write(s.project.titles.feature_title, "Benefits:")
    with st_list(s.large, s.large, list_type="ul") as l:
        with l.item():
            st_write(s.large, (s.bold, "Minimalist"), ": No classes or complexity")
        with l.item():
            st_write(s.large, (s.bold, "Flexible"), ": Can override style per-call")
        with l.item():
            st_write(s.large, (s.bold, "Intuitive"), ": Just call the function")
        with l.item():
            st_write(s.large, "Works with Config Injection")

    st_space("v", 2)

    # ========================================================================
    # PATTERN 3: OOP INHERITANCE (Advanced)
    # ========================================================================
    st_write(s.project.titles.section_title, "Pattern 3: OOP Inheritance (Advanced)")
    st_space("v", 1)

    show_explanation("""
For advanced use cases: override helpers with custom logic.

Subclass BlockHelper or ProjectBlockHelper.

Add custom methods specific to your project.
    """)

    st_write(s.project.titles.feature_title, "How it works:")
    with st_list(s.large, s.large, list_type="ol") as l:
        with l.item():
            st_write(s.large, "Subclass ", (s.bold, "BlockHelper"), " or ", (s.bold, "ProjectBlockHelper"))
        with l.item():
            st_write(s.large, "Override methods to add custom logic")
        with l.item():
            st_write(s.large, "Add new project-specific methods")
        with l.item():
            st_write(s.large, "Instantiate and use in your blocks")

    st_write(s.project.titles.feature_title, "Code example:")
    show_code("""
from streamtex import BlockHelper
from custom.styles import Styles as s

class MyCustomHelper(BlockHelper):
    # Override parent method
    def show_code(self, code, language="python"):
        print(f"About to show code in {language}")  # Custom logic!
        return super().show_code(code, language)

    # Add new project-specific method
    def show_comparison(self, before, after):
        '''Compare two code snippets.'''
        st_write(s.large, "Before:")
        self.show_code(before)
        st_write(s.large, "After:")
        self.show_code(after)

# Usage
helper = MyCustomHelper()
helper.show_code("print('hello')")
helper.show_comparison("old_code()", "new_code()")
    """, language="python")

    st_write(s.project.titles.feature_title, "Benefits:")
    with st_list(s.large, s.large, list_type="ul") as l:
        with l.item():
            st_write(s.large, (s.bold, "Extensible"), ": Add custom logic before/after parent calls")
        with l.item():
            st_write(s.large, (s.bold, "Organized"), ": Group related helpers in a class")
        with l.item():
            st_write(s.large, (s.bold, "Type-safe"), ": IDEs can autocomplete methods")
        with l.item():
            st_write(s.large, (s.bold, "Chainable"), ": Use super() to leverage parent behavior")

    st_space("v", 2)

    # ========================================================================
    # PATTERN 4: EXPERT (Bonus)
    # ========================================================================
    st_write(s.project.titles.section_title, "Pattern 4: Expert (All 3 Combined)")
    st_space("v", 1)

    show_explanation("""
For power users: combine all 3 patterns.

Use Config Injection + OOP Inheritance + Function overrides.

Maximum flexibility when you need it.
    """)

    st_write(s.project.titles.feature_title, "How it works:")
    with st_list(s.large, s.large, list_type="ol") as l:
        with l.item():
            st_write(s.large, (s.bold, "Config Injection"), " provides global styles (Pattern 1)")
        with l.item():
            st_write(s.large, (s.bold, "OOP class"), " adds custom methods (Pattern 3)")
        with l.item():
            st_write(s.large, (s.bold, "Function calls"), " can still override with style= (Pattern 2)")
        with l.item():
            st_write(s.large, "Chain everything together")

    st_write(s.project.titles.feature_title, "Code example:")
    show_code("""
from blocks.helpers import ExpertBlockHelper

# ExpertBlockHelper combines all patterns
expert = ExpertBlockHelper()

# Uses config styles (DI)
expert.show_code("print('hello')")

# Custom method (OOP)
expert.show_advanced_comparison("old", "new")

# Runtime override (Function)
from streamtex import show_code
show_code("print('world')", style=s.custom.style)
    """, language="python")

    st_write(s.project.titles.feature_title, "When to use:")
    with st_list(s.large, s.large, list_type="ul") as l:
        with l.item():
            st_write(s.large, "Complex projects with varied requirements")
        with l.item():
            st_write(s.large, "Need both global config + custom logic")
        with l.item():
            st_write(s.large, "Runtime overrides for special cases")
        with l.item():
            st_write(s.large, "Advanced developers who understand all patterns")

    st_space("v", 2)

    # ========================================================================
    # COMPARISON TABLE
    # ========================================================================
    st_write(s.project.titles.section_title, "Pattern Comparison")
    st_space("v", 1)

    show_details("""
Comparison of all patterns.

Choose based on your project's needs and complexity level.
    """)

    with st_list(s.large, s.large, list_type="ul") as l:
        with l.item():
            st_write(s.large, (s.bold, "Pattern 1 (Config Injection)"),
                     " — Complexity: Easy. Setup: One config class + set_block_helper_config(). Use when: Most projects, simple to medium complexity")
        with l.item():
            st_write(s.large, (s.bold, "Pattern 2 (Standalone Functions)"),
                     " — Complexity: Very Easy. Setup: Just import and call. Use when: Minimal setup, direct function usage")
        with l.item():
            st_write(s.large, (s.bold, "Pattern 3 (OOP Inheritance)"),
                     " — Complexity: Advanced. Setup: Subclass BlockHelper, override methods. Use when: Need custom logic, organize helpers")
        with l.item():
            st_write(s.large, (s.bold, "Pattern 4 (Expert)"),
                     " — Complexity: Very Advanced. Setup: Config + Class + Runtime overrides. Use when: Maximum flexibility needed")

    st_space("v", 2)

    # ========================================================================
    # BEST PRACTICES
    # ========================================================================
    st_write(s.project.titles.section_title, "Best Practices")
    st_space("v", 1)

    show_explanation("""
Guidelines for using block helpers effectively.

Follow these to keep your helpers clean and maintainable.
    """)

    with st_list(s.large, s.large, list_type="ol") as l:
        with l.item():
            st_write(s.large, (s.bold, "Start with Pattern 1"), " (Config Injection)")
            with st_list(s.medium, s.medium, list_type="ul") as sub:
                with sub.item():
                    st_write(s.medium, "It covers 90% of use cases")
                with sub.item():
                    st_write(s.medium, "Simple to understand and maintain")
        with l.item():
            st_write(s.large, (s.bold, "Add project-specific helpers"))
            with st_list(s.medium, s.medium, list_type="ul") as sub:
                with sub.item():
                    st_write(s.medium, "Create helpers unique to your project")
                with sub.item():
                    st_write(s.medium, "Keep them in blocks/helpers.py")
        with l.item():
            st_write(s.large, (s.bold, "Only use OOP when you need it"))
            with st_list(s.medium, s.medium, list_type="ul") as sub:
                with sub.item():
                    st_write(s.medium, "Don't over-engineer simple cases")
                with sub.item():
                    st_write(s.medium, "Use when you have custom logic to add")
        with l.item():
            st_write(s.large, (s.bold, "Document your helpers"))
            with st_list(s.medium, s.medium, list_type="ul") as sub:
                with sub.item():
                    st_write(s.medium, "Add docstrings explaining purpose")
                with sub.item():
                    st_write(s.medium, "Show usage examples in docstrings")
        with l.item():
            st_write(s.large, (s.bold, "Keep helper functions pure"))
            with st_list(s.medium, s.medium, list_type="ul") as sub:
                with sub.item():
                    st_write(s.medium, "Same input → same output")
                with sub.item():
                    st_write(s.medium, "No side effects (unless intentional)")

    st_space("v", 2)

    # ========================================================================
    # LIVE DEMONSTRATION
    # ========================================================================
    st_write(s.project.titles.section_title, "Live Demonstration")
    st_space("v", 1)

    st_write(s.large, """
Each pattern demonstrated with actual code below:
    """)

    # Demo 1: Simple pattern
    st_write(s.project.titles.subsection_title, "Demo 1: Simple Pattern")
    demonstrate_simple_pattern()

    st_space("v", 1)

    # Demo 2: Config pattern
    st_write(s.project.titles.subsection_title, "Demo 2: Config Injection Pattern")
    demonstrate_config_pattern()

    st_space("v", 1)

    # Demo 3: OOP pattern
    st_write(s.project.titles.subsection_title, "Demo 3: OOP Pattern")
    demonstrate_oop_pattern()

    st_space("v", 1)

    # Demo 4: Expert pattern
    st_write(s.project.titles.subsection_title, "Demo 4: Expert Pattern (All Combined)")
    demonstrate_expert_pattern()

    st_space("v", 2)

    # ========================================================================
    # SUMMARY
    # ========================================================================
    st_write(s.project.titles.section_title, "Summary")
    st_space("v", 1)

    show_explanation("""
Block helpers are a flexible system for rendering styled content.

4 patterns available from simple to advanced.

Choose what works for your project.
    """)

    st_write(s.project.titles.feature_title, "Recommended path:")
    with st_list(s.large, s.large, list_type="ol") as l:
        with l.item():
            st_write(s.large, "Start with ", (s.bold, "Config Injection"), " (Pattern 1)")
        with l.item():
            st_write(s.large, "Add project-specific helpers")
        with l.item():
            st_write(s.large, "Use ", (s.bold, "OOP"), " only if needed (Pattern 3)")
        with l.item():
            st_write(s.large, "Expert pattern for edge cases")

    st_write(s.project.titles.feature_title, "Learn more:")
    with st_list(s.large, s.large, list_type="ul") as l:
        with l.item():
            st_write(s.large, "See ", (s.bold, "stx_manual_intro/blocks/helpers.py"), " for minimal example")
        with l.item():
            st_write(s.large, "See ", (s.bold, "stx_manual_advanced/blocks/helpers.py"), " for complete showcase")
        with l.item():
            st_write(s.large, "See ", (s.bold, "documentation/template_project/blocks/helpers.py"), " for annotated template")

    st_write(s.project.titles.feature_title, "Next steps:")
    with st_list(s.large, s.large, list_type="ol") as l:
        with l.item():
            st_write(s.large, "Try each pattern in a small block")
        with l.item():
            st_write(s.large, "Find your preferred pattern")
        with l.item():
            st_write(s.large, "Build your project's helpers")
