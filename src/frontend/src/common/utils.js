export const getCurrentDate = () => {
    return (new Date()).toISOString().substring(0, 10);
};

export const flat2Tree = (items, id = null, link = 'chief_id') =>
    items.filter(
        item => item[link] === id
    ).map(
        item => ({
            ...item,
            key: `employee_${item.id}`,
            label: `${item.first_name} ${item.last_name} (${item.position})`,
            nodes: flat2Tree(items, item.id)
        })
    );