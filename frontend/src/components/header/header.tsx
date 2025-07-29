import React from "react";

type HeaderProps = {
    onMenuClick: () => void;
    logoSrc: string;
    logoAlt?: string;
    onNotificationsClick?: () => void;
};

const Header: React.FC<HeaderProps> = ({
    onMenuClick,
    logoSrc,
    logoAlt = "Logo",
    onNotificationsClick,
}) => (
    <header style={styles.header}>
        <button
            style={styles.menuButton}
            onClick={onMenuClick}
            aria-label="Abrir menu"
        >
            <span style={styles.hamburgerLine}></span>
            <span style={styles.hamburgerLine}></span>
            <span style={styles.hamburgerLine}></span>
        </button>
        <img src={logoSrc} alt={logoAlt} style={styles.logo} />
        <button
            style={styles.notificationsButton}
            onClick={onNotificationsClick}
            aria-label="Notificações"
        >
            <svg
                width="24"
                height="24"
                fill="none"
                viewBox="0 0 24 24"
                style={{ display: "block" }}
            >
                <path
                    d="M12 22a2 2 0 0 0 2-2h-4a2 2 0 0 0 2 2zm6-6V11a6 6 0 1 0-12 0v5l-2 2v1h16v-1l-2-2z"
                    fill="#333"
                />
            </svg>
        </button>
    </header>
);

const styles: { [key: string]: React.CSSProperties } = {
    header: {
        display: "flex",
        alignItems: "center",
        height: 64,
        padding: "0 16px",
        background: "#fff",
        boxShadow: "0 2px 4px rgba(0,0,0,0.05)",
        position: "relative",
        zIndex: 10,
    },
    menuButton: {
        background: "none",
        border: "none",
        padding: 8,
        cursor: "pointer",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        marginRight: 16,
        height: 40,
        width: 40,
    },
    hamburgerLine: {
        width: 24,
        height: 3,
        background: "#333",
        margin: "3px 0",
        borderRadius: 2,
        transition: "all 0.2s",
    },
    logo: {
        height: 40,
        objectFit: "contain",
        flex: 1,
    },
    notificationsButton: {
        background: "none",
        border: "none",
        padding: 8,
        cursor: "pointer",
        marginLeft: 16,
        height: 40,
        width: 40,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
    },
};

export default Header;
