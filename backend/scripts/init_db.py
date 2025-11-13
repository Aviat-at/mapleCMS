"""Initialize database with sample data."""

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, init_db
from app.core.security import get_password_hash
from app.models.user import User
from app.models.category import Category
from app.models.tag import Tag
from app.models.article import Article


async def create_sample_data():
    """Create sample data for development."""
    async with AsyncSessionLocal() as db:
        # Create admin user
        admin = User(
            username="admin",
            email="admin@maplecms.com",
            password_hash=get_password_hash("admin123"),
            role="admin",
            is_active=True,
        )
        db.add(admin)
        
        # Create editor user
        editor = User(
            username="editor",
            email="editor@maplecms.com",
            password_hash=get_password_hash("editor123"),
            role="editor",
            is_active=True,
        )
        db.add(editor)
        
        # Create author user
        author = User(
            username="author",
            email="author@maplecms.com",
            password_hash=get_password_hash("author123"),
            role="author",
            is_active=True,
        )
        db.add(author)
        
        await db.flush()
        
        # Create categories
        tutorial_cat = Category(
            name="Tutorial",
            slug="tutorial",
            description="Step-by-step guides and tutorials",
        )
        db.add(tutorial_cat)
        
        news_cat = Category(
            name="News",
            slug="news",
            description="Latest news and updates",
        )
        db.add(news_cat)
        
        await db.flush()
        
        # Create tags
        fastapi_tag = Tag(name="FastAPI", slug="fastapi")
        db.add(fastapi_tag)
        
        python_tag = Tag(name="Python", slug="python")
        db.add(python_tag)
        
        nextjs_tag = Tag(name="Next.js", slug="nextjs")
        db.add(nextjs_tag)
        
        await db.flush()
        
        # Create sample articles
        article1 = Article(
            title="Welcome to MapleCMS",
            slug="welcome-to-maplecms",
            excerpt="An introduction to MapleCMS - the world's lightest open-source CMS",
            content_md="# Welcome to MapleCMS\n\nMapleCMS is a modern, lightweight CMS built with FastAPI and Next.js.",
            content_html="<h1>Welcome to MapleCMS</h1><p>MapleCMS is a modern, lightweight CMS built with FastAPI and Next.js.</p>",
            status="published",
            author_id=admin.id,
            category_id=news_cat.id,
        )
        db.add(article1)
        
        article2 = Article(
            title="Getting Started with FastAPI",
            slug="getting-started-with-fastapi",
            excerpt="Learn how to build modern APIs with FastAPI",
            content_md="# Getting Started with FastAPI\n\nFastAPI is a modern, fast web framework for building APIs.",
            content_html="<h1>Getting Started with FastAPI</h1><p>FastAPI is a modern, fast web framework for building APIs.</p>",
            status="published",
            author_id=author.id,
            category_id=tutorial_cat.id,
        )
        db.add(article2)
        
        await db.commit()
        
        print("✅ Sample data created successfully!")
        print("\nTest Users:")
        print("  Admin: admin@maplecms.com / admin123")
        print("  Editor: editor@maplecms.com / editor123")
        print("  Author: author@maplecms.com / author123")


async def main():
    """Main function."""
    print("Initializing database...")
    await init_db()
    print("✅ Database initialized!")
    
    print("\nCreating sample data...")
    await create_sample_data()


if __name__ == "__main__":
    asyncio.run(main())
